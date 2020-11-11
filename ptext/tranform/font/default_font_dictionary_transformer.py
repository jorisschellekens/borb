from typing import Optional, List

from ptext.object.canvas.font.font import Font
from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_dictionary import PDFDictionary
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultFontDictionaryTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return (
            isinstance(object, PDFDictionary)
            and PDFName("Type") in object
            and object[PDFName("Type")] == PDFName("Font")
        )

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

        # convert dictionary like structure
        tmp = Font()
        tmp.parent = parent_object

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # convert key/value pair(s)
        for k, v in object_to_transform.items():
            if k == PDFName("Parent"):
                continue
            v = self.get_root_transformer().transform(v, tmp, context, [])
            if v != PDFNull():
                tmp.set(k.name, v)

        # return
        return tmp
