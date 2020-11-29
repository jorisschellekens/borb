from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_object import PDFObject, PDFIndirectObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultIndirectObjectTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFIndirectObject to a List / Dictionary / primitive object
    """

    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFIndirectObject)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:
        return self.get_root_transformer().transform(
            object_to_transform.get_object(), parent_object, context, event_listeners
        )
