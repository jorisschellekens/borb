#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Image objects
"""
import io
import typing

from PIL import Image as PILImageModule

from borb.io.read.pdf_object import PDFObject
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState


class ImageTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Image objects
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _convert_to_rgb_mode(self, image: PILImageModule.Image) -> PILImageModule.Image:
        # build image_out
        image_out: PILImageModule.Image = image

        # omit transparency
        if image_out.mode == "P":
            image_out = image_out.convert("RGBA")
        if image_out.mode == "LA":
            image_out = image_out.convert("RGBA")
        if image_out.mode == "RGBA":
            fill_color = (255, 255, 255)  # new background color
            non_alpha_mode: str = image_out.mode[:-1]
            background = PILImageModule.new(
                non_alpha_mode, image_out.size, fill_color  # type: ignore[arg-type]
            )
            background.paste(image_out, mask=image_out.split()[-1])  # omit transparency
            image_out = background

        # convert to RGB
        image_out = image_out.convert("RGB")

        # add methods
        PDFObject.add_pdf_object_methods(image_out)
        image_out.set_reference(image.get_reference())  # type: ignore[attr-defined]

        # return
        return image_out

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is an Image
        :param object:  the object to be transformed
        :return:        True if the object is an Image, False otherwise
        """
        return isinstance(object, PILImageModule.Image)

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
        assert isinstance(object_to_transform, PILImageModule.Image), "object_to_transform must be of type PIL.Image.Image"
        # fmt: on

        # get image bytes
        contents: typing.Optional[bytes] = None
        filter_name: typing.Optional[Name] = None
        try:
            with io.BytesIO() as output:
                assert isinstance(object_to_transform, PILImageModule.Image)
                # TODO: find a better solution than converting everything to mode RGB
                object_to_transform = self._convert_to_rgb_mode(object_to_transform)  # type: ignore[assignment]
                assert isinstance(object_to_transform, PILImageModule.Image)
                object_to_transform.save(output, format="JPEG")
                contents = output.getvalue()
            filter_name = Name("DCTDecode")
        except Exception as e:
            pass

        # check that the image has some byte-representation
        assert contents is not None

        # build corresponding Stream (XObject)
        out_value = Stream()
        out_value[Name("Type")] = Name("XObject")
        out_value[Name("Subtype")] = Name("Image")
        out_value[Name("Width")] = bDecimal(object_to_transform.width)
        out_value[Name("Height")] = bDecimal(object_to_transform.height)
        out_value[Name("Length")] = bDecimal(len(contents))
        out_value[Name("Filter")] = filter_name
        out_value[Name("BitsPerComponent")] = bDecimal(8)
        out_value[Name("ColorSpace")] = Name("DeviceRGB")
        out_value[Name("Bytes")] = contents

        # copy reference
        out_value.set_reference(
            object_to_transform.get_reference()  # type: ignore[union-attr]
        )

        # start object if needed
        started_object = False
        ref = out_value.get_reference()  # type: ignore[attr-defined]
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
