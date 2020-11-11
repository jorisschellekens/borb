from typing import Optional, List

from ptext.object.canvas.font.font import Font
from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_dictionary import PDFDictionary
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.default_dictionary_transformer import DefaultDictionaryTransformer


class DefaultFontDescriptorDictionaryTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return (
            isinstance(object, PDFDictionary)
            and PDFName("Type") in object
            and object[PDFName("Type")] == PDFName("FontDescriptor")
        )

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

        # convert like regular dictionary
        if isinstance(parent_object, Font):
            for t in self.get_root_transformer().handlers:
                if isinstance(t, DefaultDictionaryTransformer):
                    return t.transform(
                        object_to_transform, parent_object, context, event_listeners
                    )

        # build intermittent Font object
        tmp = Font()

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        tmp.set(
            "FontDescriptor",
            self.get_root_transformer().transform(
                object_to_transform, tmp, context, []
            ),
        )

        # return
        return tmp
