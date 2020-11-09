from typing import Optional, List

from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_indirect_reference import PDFIndirectReference
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject
from ptext.primitive.pdf_string import PDFLiteralString
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultReferenceTransformer(BaseTransformer):
    def __init__(self):
        self.cache = {}
        self.ref_count = {}

    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFIndirectReference)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

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
            return PDFNull()

        # lookup in cache
        if ref_uuid in self.cache:
            return self.cache[ref_uuid]

        # lookup xref
        xref = context.root_object.get(["XRef"])
        src = context.source
        tok = context.tokenizer

        # get reference
        val = xref.get_object_for_indirect_reference(object_to_transform, src, tok)

        # transform
        context.indirect_reference_chain.append(ref_uuid)
        val = self.get_root_transformer().transform(
            val, parent_object, context, event_listeners
        )
        if val is not None and isinstance(val, PDFHighLevelObject):
            val.set("ObjectNumber", PDFLiteralString(ref_uuid))
        context.indirect_reference_chain.pop(-1)

        # update cache
        if val is not None:
            self.cache[ref_uuid] = val

        # return
        return val
