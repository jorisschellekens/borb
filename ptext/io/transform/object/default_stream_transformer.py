import io
import typing
from typing import Optional, Any, Union

from ptext.io.filter.stream_decode_util import decode_stream
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import (
    Dictionary,
    Stream,
    Reference,
    AnyPDFType,
)
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultStreamTransformer(BaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, Stream)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        tmp = Dictionary().set_parent(parent_object)

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # resolve references in stream dictionary
        assert context is not None
        assert context.tokenizer is not None
        assert isinstance(object_to_transform, Stream)
        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.items():
            if isinstance(v, Reference):
                v = xref.get(v, context.tokenizer.io_source, context.tokenizer)
                object_to_transform[k] = v

        # apply filter(s)
        object_to_transform = decode_stream(object_to_transform)

        # convert (remainder of) stream dictionary
        for k, v in object_to_transform.items():
            if not isinstance(v, Reference):
                v = self.get_root_transformer().transform(v, tmp, context, [])
                if v is not None:
                    object_to_transform[k] = v

        # linkage
        object_to_transform.set_parent(parent_object)

        # return
        return object_to_transform
