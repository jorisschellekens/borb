import io
import typing
from typing import Optional, Any, Union

from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    TransformerContext,
)
from ptext.io.read_transform.types import Reference, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.pdf.xref.xref import XREF


class DefaultReferenceTransformer(ReadBaseTransformer):
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
        if (
            object_to_transform.parent_stream_object_number is not None
            and object_to_transform.index_in_parent_stream is not None
        ):
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
        assert context.root_object is not None
        xref = context.root_object["XRef"]
        assert xref is not None
        assert isinstance(xref, XREF)

        src = context.source
        assert src is not None

        tok = context.tokenizer
        assert tok is not None

        # get reference
        referenced_object = xref.get_object(object_to_transform, src, tok)
        if referenced_object is None:
            return None

        # transform
        assert referenced_object is not None
        context.indirect_reference_chain.append(ref_uuid)
        transformed_referenced_object = self.get_root_transformer().transform(
            referenced_object, parent_object, context, event_listeners
        )
        context.indirect_reference_chain.pop(-1)

        # update cache
        if transformed_referenced_object is not None:
            self.cache[ref_uuid] = transformed_referenced_object

        # return
        return transformed_referenced_object
