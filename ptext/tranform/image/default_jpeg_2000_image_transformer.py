import io
from typing import Optional, List, Any

from PIL import Image

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject
from ptext.primitive.pdf_stream import PDFStream
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import add_base_methods


@add_base_methods
class DefaultJPEG2000ImageTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return (
            isinstance(object, PDFStream)
            and (
                (
                    PDFName("Type") in object.stream_dictionary
                    and object.stream_dictionary[PDFName("Type")] == PDFName("XObject")
                )
                or PDFName("Type") not in object.stream_dictionary
            )
            and PDFName("Subtype") in object.stream_dictionary
            and object.stream_dictionary[PDFName("Subtype")] == PDFName("Image")
            and PDFName("Filter") in object.stream_dictionary
            and (
                object.stream_dictionary[PDFName("Filter")] == PDFName("JPXDecode")
                or (
                    isinstance(object.stream_dictionary[PDFName("Filter")], PDFArray)
                    and object.stream_dictionary[PDFName("Filter")][0]
                    == PDFName("JPXDecode")
                )
            )
        )

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        # use PIL to read image bytes
        try:
            tmp = Image.open(io.BytesIO(object_to_transform.raw_byte_array))
            tmp.getpixel(
                (0, 0)
            )  # attempting to read pixel 0,0 will trigger an error if the underlying image does not exist
        except:
            w = object_to_transform.stream_dictionary[PDFName("Width")].get_int_value()
            h = object_to_transform.stream_dictionary[PDFName("Height")].get_int_value()
            tmp = Image.new("RGB", (w, h), (128, 128, 128))

        # add base methods
        add_base_methods(tmp.__class__)

        # set parent
        tmp.set_parent(parent_object)

        # add event listeners
        for l in event_listeners:
            tmp.add_event_listener(l)

        # return
        return tmp
