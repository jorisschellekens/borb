import io
import typing
from typing import Optional, Any, Union

from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    TransformerContext,
)
from ptext.io.read_transform.types import (
    String,
    HexadecimalString,
    Name,
    AnyPDFType,
)
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadStringTransformer(ReadBaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, String)
            or isinstance(object, HexadecimalString)
            or isinstance(object, Name)
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        # set parent
        object_to_transform.set_parent(parent_object)  # type: ignore[union-attr]
        # return
        return object_to_transform
