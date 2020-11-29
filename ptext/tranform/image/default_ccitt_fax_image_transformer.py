from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject
from ptext.primitive.pdf_stream import PDFStream
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultCCITTFaxImageTransformer(BaseTransformer):
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
                object.stream_dictionary[PDFName("Filter")] == PDFName("CCITTFaxDecode")
                or (
                    isinstance(object.stream_dictionary[PDFName("Filter")], PDFArray)
                    and object.stream_dictionary[PDFName("Filter")][0]
                    == PDFName("CCITTFaxDecode")
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

        # TODO
        return None
