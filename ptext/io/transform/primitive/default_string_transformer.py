from typing import Optional, List, Any, Union

from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.tokenize.types.pdf_string import PDFString, PDFLiteralString, PDFHexString
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import (
    StringWithParentAttribute,
    HexStringWithParentAttribute,
)


class DefaultStringTransformer(BaseTransformer):
    def can_be_transformed(self, object: Union["io.IOBase", "PDFObject"]) -> bool:
        return isinstance(object, PDFString)

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "PDFObject"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:
        if isinstance(object_to_transform, PDFLiteralString):
            return StringWithParentAttribute(object_to_transform.text).set_parent(
                parent_object
            )
        if isinstance(object_to_transform, PDFHexString):
            return HexStringWithParentAttribute(object_to_transform.text).set_parent(
                parent_object
            )
        return None
