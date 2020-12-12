import io
from typing import Optional, List, Any, Union

from PIL import Image

from ptext.io.tokenize.types.pdf_array import PDFArray
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_stream import PDFStream
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import add_base_methods


@add_base_methods
class DefaultJPEGImageTransformer(BaseTransformer):
    def can_be_transformed(self, object: Union["io.IOBase", "PDFObject"]) -> bool:
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
                object.stream_dictionary[PDFName("Filter")] == PDFName("DCTDecode")
                or (
                    isinstance(object.stream_dictionary[PDFName("Filter")], PDFArray)
                    and object.stream_dictionary[PDFName("Filter")][0]
                    == PDFName("DCTDecode")
                )
            )
        )

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "PDFObject"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        # use PIL to read image bytes
        tmp = Image.open(io.BytesIO(object_to_transform.raw_byte_array))

        # add base methods
        add_base_methods(tmp.__class__)

        # set parent
        tmp.set_parent(parent_object)

        # add event listeners
        for l in event_listeners:
            tmp.add_event_listener(l)

        # return
        return tmp
