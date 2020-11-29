from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import DecimalWithParentAttribute


class DefaultNumberTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts PDFInt and PDFFloat to Decimal
    """

    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFNumber)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:
        return DecimalWithParentAttribute(
            object_to_transform.get_float_value()
        ).set_parent(parent_object)
