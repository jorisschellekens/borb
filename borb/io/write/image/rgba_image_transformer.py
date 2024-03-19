#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing RGBA Image objects
"""
import itertools
import typing
import zlib

from PIL import Image as PILImageModule

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState


class RGBAImageTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing RGBA Image objects
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _construct_smask_stream(image: PILImageModule.Image) -> Stream:
        # get raw <alpha> bytes
        w: int = image.width
        h: int = image.height
        smask_bytes: bytes = bytes([a for r, g, b, a in image.getdata()])

        # compression
        smask_compressed_bytes = zlib.compress(smask_bytes)

        # construct output value
        out: Stream = Stream()
        out[Name("BitsPerComponent")] = bDecimal(8)
        out[Name("Bytes")] = smask_compressed_bytes
        out[Name("ColorSpace")] = Name("DeviceGray")
        out[Name("Filter")] = Name("FlateDecode")
        out[Name("Height")] = bDecimal(h)
        out[Name("Length")] = bDecimal(len(smask_compressed_bytes))
        out[Name("Subtype")] = Name("Image")
        out[Name("Type")] = Name("XObject")
        out[Name("Width")] = bDecimal(w)
        return out

    @staticmethod
    def _rgb_array(image: PILImageModule.Image) -> bytes:
        s0 = [(r, g, b) for r, g, b, a in image.getdata()]
        s1 = [x for x in itertools.chain(*s0)]
        return bytes(s1)

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is an Image
        :param object:  the object to be transformed
        :return:        True if the object is an Image, False otherwise
        """
        return isinstance(object, PILImageModule.Image) and object.mode == "RGBA"

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms an Image into a byte stream
        :param object_to_transform:     the Image to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Image
        """

        # fmt: off
        assert (context is not None), "context must be defined in order to write Image objects."
        assert context.destination is not None, "context.destination must be defined in order to write Image objects."
        assert isinstance(object_to_transform, PILImageModule.Image), "object_to_transform must be of type PILImage.Image"
        # fmt: on

        # construct SMask entry
        smask_img: Stream = RGBAImageTransformer._construct_smask_stream(
            object_to_transform
        )
        smask_img.set_is_inline(False)
        smask_img.set_is_unique(True)
        self.get_reference(smask_img, context)
        self._start_object(smask_img, context)
        self.get_root_transformer().transform(smask_img, context)
        self._end_object(smask_img, context)

        # build corresponding Stream (XObject)
        rgb_bytes: bytes = RGBAImageTransformer._rgb_array(object_to_transform)
        out_value = Stream()
        out_value[Name("BitsPerComponent")] = bDecimal(8)
        out_value[Name("Bytes")] = zlib.compress(rgb_bytes)
        out_value[Name("ColorSpace")] = Name("DeviceRGB")
        out_value[Name("Filter")] = Name("FlateDecode")
        out_value[Name("Height")] = bDecimal(object_to_transform.height)
        out_value[Name("Length")] = bDecimal(len(out_value[Name("Bytes")]))
        out_value[Name("SMask")] = smask_img
        out_value[Name("Subtype")] = Name("Image")
        out_value[Name("Type")] = Name("XObject")
        out_value[Name("Width")] = bDecimal(object_to_transform.width)

        # copy reference
        out_value.set_reference(  # type: ignore[attr-defined]
            object_to_transform.get_reference()  # type: ignore [union-attr]
        )

        # start object if needed
        started_object = False
        ref = out_value.get_reference()  # type: ignore [attr-defined]
        if ref is not None:
            assert isinstance(ref, Reference)
            if ref.object_number is not None and ref.byte_offset is None:
                started_object = True
                self._start_object(out_value, context)

        # write stream
        cl = context.compression_level
        context.compression_level = 9
        self.get_root_transformer().transform(out_value, context)
        context.compression_level = cl

        # end object if needed
        if started_object:
            self._end_object(out_value, context)
