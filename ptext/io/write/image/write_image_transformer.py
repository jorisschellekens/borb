#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of WriteBaseTransformer is responsible for writing Image objects
"""
import io
from typing import Optional

from PIL import Image as PILImage  # type: ignore [import]

from ptext.io.read.types import AnyPDFType, Name, Stream, Reference, add_base_methods
from ptext.io.read.types import Decimal as pDecimal
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteImageTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Image objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents an Image object
        """
        return isinstance(any, PILImage.Image)

    def _convert_png_to_jpg(self, image: PILImage.Image) -> PILImage.Image:

        # omit transparency
        fill_color = (255, 255, 255)  # new background color
        image_out = image.convert("RGBA")  # it had mode P after DL it from OP
        if image_out.mode in ("RGBA", "LA"):
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
        context: Optional[WriteTransformerContext] = None,
    ):
        """
        This method writes an Image to a byte stream
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, PILImage.Image)

        # get image bytes
        contents = None
        filter_name: Optional[Name] = None
        try:
            with io.BytesIO() as output:
                assert isinstance(object_to_transform, PILImage.Image)
                object_to_transform.save(output, format="JPEG")
                contents = output.getvalue()
            filter_name = Name("DCTDecode")
        except Exception as e:
            pass

        if contents is None:
            try:
                # TODO : properly store PNG (instead of converting it)
                with io.BytesIO() as output:
                    object_to_transform = self._convert_png_to_jpg(object_to_transform)
                    assert isinstance(object_to_transform, PILImage.Image)
                    object_to_transform.save(output, format="JPEG")
                    contents = output.getvalue()
                filter_name = Name("DCTDecode")
            except Exception as e:
                pass
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
