from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import StringWithParentAttribute


class DefaultNameTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts PDFName to str
    """

    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFName)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:
        return StringWithParentAttribute(object_to_transform.name).set_parent(
            parent_object
        )
