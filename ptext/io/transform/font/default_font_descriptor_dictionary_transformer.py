from typing import Optional, List, Any, Union

from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.io.tokenize.types.pdf_dictionary import PDFDictionary

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.object.default_dictionary_transformer import DefaultDictionaryTransformer


class DefaultFontDescriptorDictionaryTransformer(BaseTransformer):
    def can_be_transformed(self, object: Union["io.IOBase", "PDFObject"]) -> bool:
        return (
            isinstance(object, PDFDictionary)
            and PDFName("Type") in object
            and object[PDFName("Type")] == PDFName("FontDescriptor")
        )

    def transform(
        self,
        object_to_transform: Union["io.IOBase", "PDFObject"],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> Any:

        # convert like regular dictionary
        if isinstance(parent_object, Font):
            for t in self.get_root_transformer().handlers:
                if isinstance(t, DefaultDictionaryTransformer):
                    return t.transform(
                        object_to_transform, parent_object, context, event_listeners
                    )

        # build intermittent Font object
        tmp = Font().set_parent(parent_object)

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        tmp["FontDescriptor"] = self.get_root_transformer().transform(
            object_to_transform, tmp, context, []
        )

        # return
        return tmp
