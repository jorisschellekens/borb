import io
from typing import Optional

from PIL.Image import Image  # type: ignore [import]

from ptext.io.read.types import AnyPDFType, Name, Stream, Decimal, Reference
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteImageTransformer(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Image)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Image)

        # check whether image has alpha
        # IF image has alpha --> write image as PNG
        # ELSE --> write image as JPEG

        has_alpha = False
        if object_to_transform.mode == "RGBA":
            has_alpha = True
        if object_to_transform.mode == "P":
            transparency_index = object_to_transform.info.get("transparency", -1)
            for _, index in object_to_transform.getcolors():
                if index == transparency_index:
                    has_alpha = True
                    break

        # get image bytes
        format = "PNG" if has_alpha else "JPEG"
        contents = None
        with io.BytesIO() as output:
            object_to_transform.save(output, format=format)
            contents = output.getvalue()

        # build corresponding Stream (XObject)
        out_value = Stream()
        out_value[Name("Type")] = Name("XObject")
        out_value[Name("Subtype")] = Name("Image")
        out_value[Name("Width")] = Decimal(object_to_transform.width)
        out_value[Name("Height")] = Decimal(object_to_transform.height)
        out_value[Name("Length")] = Decimal(len(contents))
        out_value[Name("Filter")] = Name("DCTDecode")
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
