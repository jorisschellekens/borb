#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Image objects
"""
import io
import typing
from typing import Optional

from PIL import Image as PILImage  # type: ignore [import]

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as pDecimal
from borb.io.read.types import Name, Reference, Stream, add_base_methods
from borb.io.write.transformer import Transformer, WriteTransformerState


class ImageTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Image objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents an Image object
        """
        return isinstance(any, PILImage.Image)

    def _convert_to_rgb_mode(self, image: PILImage.Image) -> PILImage.Image:

        # build image_out
        image_out: PILImage.Image = image

        # omit transparency
        if image_out.mode == "P":
            image_out = image_out.convert("RGBA")
        if image_out.mode in ["RGBA", "LA"]:
            fill_color = (255, 255, 255)  # new background color
            background = PILImage.new(image_out.mode[:-1], image_out.size, fill_color)
            background.paste(image_out, image_out.split()[-1])  # omit transparency
            image_out = background

        # convert to RGB
        image_out = image_out.convert("RGB")

        # add methods
        add_base_methods(image_out)
        image_out.set_reference(image.get_reference())

        # return
        return image_out

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes an Image to a byte stream
        """
        assert (
            context is not None
        ), "A WriteTransformerState must be defined in order to write Image objects."
        assert context.destination is not None
        assert isinstance(object_to_transform, PILImage.Image)

        # get image bytes
        contents: typing.Optional[bytes] = None
        filter_name: Optional[Name] = None
        try:
            with io.BytesIO() as output:
                assert isinstance(object_to_transform, PILImage.Image)
                object_to_transform = self._convert_to_rgb_mode(
                    object_to_transform
                )  # TODO: find a better solution than converting everything to mode RGB
                assert isinstance(object_to_transform, PILImage.Image)
                object_to_transform.save(output, format="JPEG")
                contents = output.getvalue()
            filter_name = Name("DCTDecode")
        except Exception as e:
            pass

        # assert that the image has some byte-representation
        assert contents is not None

        # build corresponding Stream (XObject)
        out_value = Stream()
        out_value[Name("Type")] = Name("XObject")
        out_value[Name("Subtype")] = Name("Image")
        out_value[Name("Width")] = pDecimal(object_to_transform.width)
        out_value[Name("Height")] = pDecimal(object_to_transform.height)
        out_value[Name("Length")] = pDecimal(len(contents))
        out_value[Name("Filter")] = filter_name
        out_value[Name("BitsPerComponent")] = pDecimal(8)
        out_value[Name("ColorSpace")] = Name("DeviceRGB")
        out_value[Name("Bytes")] = contents

        # copy reference
        out_value.set_reference(object_to_transform.get_reference())  # type: ignore [attr-defined]

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
