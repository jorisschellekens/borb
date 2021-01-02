import io
import typing
from typing import Optional, Any, Union

from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    TransformerContext,
)
from ptext.io.read_transform.types import Dictionary, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadDictionaryTransformer(ReadBaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFDictionary to a Dictionary
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, Dictionary)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # create root object
        assert isinstance(object_to_transform, Dictionary)
        object_to_transform.set_parent(parent_object)  # type: ignore [attr-defined]

        # add listener(s)
        for l in event_listeners:
            object_to_transform.add_event_listener(l)  # type: ignore [attr-defined]

        # transform key/value pair(s)
        for k, v in object_to_transform.items():
            v = self.get_root_transformer().transform(
                v, object_to_transform, context, []
            )
            if v is not None:
                object_to_transform[k] = v

        # return
        return object_to_transform
