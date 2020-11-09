from typing import Optional, List

from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_dictionary import PDFDictionary
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultDictionaryTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return isinstance(object, PDFDictionary)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

        # create root object
        tmp = PDFHighLevelObject()
        tmp.parent = parent_object

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # transform key/value pair(s)
        for k, v in object_to_transform.items():
            v = self.get_root_transformer().transform(v, tmp, context, [])
            if v != PDFNull():
                tmp.set(k.name, v)

        # return
        return tmp
