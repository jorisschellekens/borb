import typing
from typing import Optional, Any, Union

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import Decimal
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultNumberTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts PDFInt and PDFFloat to Decimal
    """

    def can_be_transformed(self, object: Union["io.IOBase", "AnyPDFType"]) -> bool:
        return isinstance(object, Decimal)

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "AnyPDFType"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        return Decimal(object_to_transform).set_parent(parent_object)
