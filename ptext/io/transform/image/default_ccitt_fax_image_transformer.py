import logging
from typing import Optional, List, Any, Union

from ptext.io.tokenize.types.pdf_array import PDFArray
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_stream import PDFStream
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext

logger = logging.getLogger(__name__)


class DefaultCCITTFaxImageTransformer(BaseTransformer):
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
        object_to_transform: Union["io.IOBase", "PDFObject"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        # TODO
        return None
