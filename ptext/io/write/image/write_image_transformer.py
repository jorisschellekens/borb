#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of WriteBaseTransformer is responsible for writing Image objects
"""
import io
from typing import Optional

from PIL.Image import Image  # type: ignore [import]

from ptext.io.read.types import AnyPDFType, Name, Stream, Decimal, Reference
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteImageTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Image objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Image)

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
        assert isinstance(object_to_transform, Image)

        # get image bytes
        contents = None
        filter_name: Optional[Name] = None
        try:
            with io.BytesIO() as output:
                object_to_transform.save(output, format="JPEG")
                contents = output.getvalue()
            filter_name = Name("DCTDecode")
        except Exception as e:
            pass

        if contents is None:
            try:
                # TODO : store PNG
                with io.BytesIO() as output:
                    object_to_transform.convert("RGB").save(output, format="JPEG")
                    contents = output.getvalue()
                filter_name = Name("DCTDecode")
            except:
                pass
        assert contents is not None

        # build corresponding Stream (XObject)
        out_value = Stream()
        out_value[Name("Type")] = Name("XObject")
        out_value[Name("Subtype")] = Name("Image")
        out_value[Name("Width")] = Decimal(object_to_transform.width)
        out_value[Name("Height")] = Decimal(object_to_transform.height)
        out_value[Name("Length")] = Decimal(len(contents))
        out_value[Name("Filter")] = filter_name
        out_value[Name("BitsPerComponent")] = Decimal(8)
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
                self.start_object(out_value, context)

        # write stream
        self.get_root_transformer().transform(out_value, context)

        # end object if needed
        if started_object:
            self.end_object(out_value, context)
