import io
import typing
from typing import Optional, Any, Union

from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read_transform.types import Reference, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.pdf.xref.xref import XREF


class DefaultReferenceTransformer(ReadBaseTransformer):
    def __init__(self):
        self.cache: typing.Dict[Reference, AnyPDFType] = {}

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, Reference)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        assert isinstance(object_to_transform, Reference)

        # check for circular reference
        assert context is not None
        if object_to_transform in context.indirect_reference_chain:
            return None

        # lookup in cache
        ref_from_cache = self.cache.get(object_to_transform, None)
        if ref_from_cache is not None:
            return ref_from_cache

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
        context.indirect_reference_chain.add(object_to_transform)
        transformed_referenced_object = self.get_root_transformer().transform(
            referenced_object, parent_object, context, event_listeners
        )
        context.indirect_reference_chain.remove(object_to_transform)

        # update cache
        if transformed_referenced_object is not None:
            self.cache[object_to_transform] = transformed_referenced_object

        # return
        return transformed_referenced_object
