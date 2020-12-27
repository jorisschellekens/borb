import io
import typing
from typing import Optional, Any, Union

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import Reference, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultReferenceTransformer(BaseTransformer):
    def __init__(self):
        self.cache = {}
        self.ref_count = {}

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, Reference)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        assert isinstance(object_to_transform, Reference)

        # canonic reference
        ref_uuid = ""
        if object_to_transform.object_number is not None:
            ref_uuid = "%d" % object_to_transform.object_number
        if object_to_transform.parent_stream_object_number is not None:
            ref_uuid = "%d/%d" % (
                object_to_transform.parent_stream_object_number,
                object_to_transform.index_in_parent_stream,
            )

        # check for circular reference
        assert context is not None
        if ref_uuid in context.indirect_reference_chain:
            return None

        # lookup in cache
        if ref_uuid in self.cache:
            return self.cache[ref_uuid]

        # lookup xref
        xref = context.root_object["XRef"]
        src = context.source
        tok = context.tokenizer

        # get reference
        val = xref.get(object_to_transform, src, tok)

        # transform
        context.indirect_reference_chain.append(ref_uuid)
        val = self.get_root_transformer().transform(
            val, parent_object, context, event_listeners
        )
        context.indirect_reference_chain.pop(-1)

        # update cache
        if val is not None:
            self.cache[ref_uuid] = val

        # return
        return val
