import io
import typing
from typing import Optional, Any, Union

from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    TransformerContext,
)
from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultIndirectObjectTransformer(ReadBaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFIndirectObject to a List / Dictionary / primitive object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return False

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # transform object
        transformed_object = self.get_root_transformer().transform(
            object_to_transform, parent_object, context, event_listeners
        )

        # copy reference
        transformed_object.set_reference(object_to_transform.get_reference())  # type: ignore  [union-attr]

        # return
        return transformed_object
