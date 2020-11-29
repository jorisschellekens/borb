from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_indirect_reference import PDFIndirectReference
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject, PDFIndirectObject
from ptext.primitive.pdf_stream import PDFStream
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import DictionaryWithParentAttribute


class DefaultStreamTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFStream)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        tmp = DictionaryWithParentAttribute().set_parent(parent_object)

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # resolve references in stream dictionary
        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.stream_dictionary.items():
            if isinstance(v, PDFIndirectReference):
                v = xref.get_object_for_indirect_reference(
                    v, context.tokenizer.io_source, context.tokenizer
                )
                if isinstance(v, PDFIndirectObject):
                    v = v.get_object()
                object_to_transform.stream_dictionary[k] = v

        # convert content
        tmp["RawBytes"] = object_to_transform.raw_byte_array
        tmp["DecodedBytes"] = object_to_transform.get_decoded_bytes()
        tmp["Type"] = "Stream"

        # convert stream dictionary
        tmp2 = self.get_root_transformer().transform(
            object_to_transform.stream_dictionary, parent_object, context, []
        )
        if not isinstance(tmp2, PDFNull):
            for k, v in tmp2.items():
                tmp[k] = v

        return tmp
