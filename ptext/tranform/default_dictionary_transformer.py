from typing import Optional, List, Any

from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_dictionary import PDFDictionary
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import DictionaryWithParentAttribute


class DefaultDictionaryTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFDictionary to a Dictionary
    """

    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFDictionary)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        # create root object
        tmp = DictionaryWithParentAttribute()
        tmp.set_parent(parent_object)

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # transform key/value pair(s)
        for k, v in object_to_transform.items():
            v = self.get_root_transformer().transform(v, tmp, context, [])
            if v != PDFNull():
                tmp[k.name] = v

        # return
        return tmp
