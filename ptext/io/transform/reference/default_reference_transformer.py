from typing import Optional, List, Any, Union

from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.tokenize.types.pdf_indirect_reference import PDFIndirectReference
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext


class DefaultReferenceTransformer(BaseTransformer):
    def __init__(self):
        self.cache = {}
        self.ref_count = {}

    def can_be_transformed(self, object: Union["io.IOBase", "PDFObject"]) -> bool:
        return isinstance(object, PDFIndirectReference)

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "PDFObject"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        # canonic reference
        ref_uuid = ""
        if object_to_transform.get_object_number() is not None:
            ref_uuid = "%d" % object_to_transform.get_object_number().get_int_value()
        if object_to_transform.get_parent_stream_number() is not None:
            ref_uuid = "%d/%d" % (
                object_to_transform.get_parent_stream_number().get_int_value,
                object_to_transform.get_index_in_stream().get_int_value(),
            )

        # check for circular reference
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
        val = xref.get_object_for_indirect_reference(object_to_transform, src, tok)

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
