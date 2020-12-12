from typing import Optional, List, Any, Union

from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import DecimalWithParentAttribute


class DefaultNumberTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts PDFInt and PDFFloat to Decimal
    """

    def can_be_transformed(self, object: Union["io.IOBase", "PDFObject"]) -> bool:
        return isinstance(object, PDFNumber)

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "PDFObject"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:
        return DecimalWithParentAttribute(
            object_to_transform.get_float_value()
        ).set_parent(parent_object)
