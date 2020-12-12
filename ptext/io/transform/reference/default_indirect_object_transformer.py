from typing import Optional, List, Any, Union

from ptext.io.tokenize.types.pdf_object import PDFIndirectObject
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext


class DefaultIndirectObjectTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFIndirectObject to a List / Dictionary / primitive object
    """

    def can_be_transformed(self, object: Union["io.IOBase", "PDFObject"]) -> bool:
        return isinstance(object, PDFIndirectObject)

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "PDFObject"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:
        return self.get_root_transformer().transform(
            object_to_transform.get_object(), parent_object, context, event_listeners
        )
