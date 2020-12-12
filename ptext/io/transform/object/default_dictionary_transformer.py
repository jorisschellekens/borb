from typing import Optional, List, Any, Union

from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.tokenize.types.pdf_dictionary import PDFDictionary
from ptext.io.tokenize.types.pdf_null import PDFNull
from ptext.io.tokenize.types.pdf_object import PDFObject
from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import DictionaryWithParentAttribute


class DefaultDictionaryTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFDictionary to a Dictionary
    """

    def can_be_transformed(self, object: Union["io.IOBase", "PDFObject"]) -> bool:
        return isinstance(object, PDFDictionary)

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "PDFObject"],
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
