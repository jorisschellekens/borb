import io
from typing import Optional, List

from ptext.object.canvas.canvas import Canvas
from ptext.object.canvas.event.begin_page_event import BeginPageEvent
from ptext.object.canvas.event.end_page_event import EndPageEvent
from ptext.object.page.page import Page
from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_dictionary import PDFDictionary
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext


class DefaultPageDictionaryTransformer(BaseTransformer):
    def can_be_transformed(self, object: PDFObject) -> bool:
        return (
            isinstance(object, PDFDictionary)
            and PDFName("Type") in object
            and object[PDFName("Type")] == PDFName("Page")
        )
        object[PDFName("Parent")] = None

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:

        # convert dictionary like structure
        tmp = Page()
        tmp.parent = parent_object

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # convert key/value pairs
        for k, v in object_to_transform.items():
            # avoid circular reference
            if k == PDFName("Parent"):
                continue
            v = self.get_root_transformer().transform(v, tmp, context, [])
            if v != PDFNull():
                tmp.set(k.name, v)

        # send out BeginPageEvent
        tmp.event_occurred(BeginPageEvent(tmp))

        # set up canvas
        contents = tmp.get("Contents")
        if contents != PDFNull():
            contents.set("Canvas", Canvas())

            # process bytes in stream
            if contents.has_key("Type") and contents.get("Type") == PDFName("Stream"):
                contents.get("Canvas").read(io.BytesIO(contents.get("DecodedBytes")))

            # process bytes in array
            if contents.has_key("Type") and contents.get("Type") == PDFName("Array"):
                l = contents.get("Length").get_int_value()
                bts = b"".join(
                    [contents.get([i, "DecodedBytes"]) + b" " for i in range(0, l)]
                )
                contents.get("Canvas").read(io.BytesIO(bts))

        # send out EndPageEvent
        tmp.event_occurred(EndPageEvent(tmp))

        # return
        return tmp
