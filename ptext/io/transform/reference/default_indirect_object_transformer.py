import typing
from typing import Optional, Any, Union

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultIndirectObjectTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFIndirectObject to a List / Dictionary / primitive object
    """

    def can_be_transformed(self, object: Union["io.IOBase", "AnyPDFType"]) -> bool:
        return False

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "AnyPDFType"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        transformed_object = self.get_root_transformer().transform(
            object_to_transform, parent_object, context, event_listeners
        )
        # copy reference
        transformed_object.set_reference(object_to_transform.get_reference())
        # return
        return transformed_object
