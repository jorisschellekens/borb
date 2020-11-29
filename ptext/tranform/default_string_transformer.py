from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_object import PDFObject
from ptext.primitive.pdf_string import PDFString, PDFLiteralString, PDFHexString
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import (
    StringWithParentAttribute,
    HexStringWithParentAttribute,
)


class DefaultStringTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFString)

    def transform(
        self,
        object_to_transform: PDFObject,
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
