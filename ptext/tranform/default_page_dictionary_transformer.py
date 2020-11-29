import io
from typing import Optional, List, Any, Union

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.canvas import Canvas
from ptext.object.canvas.event.begin_page_event import BeginPageEvent
from ptext.object.canvas.event.end_page_event import EndPageEvent
from ptext.object.page.page import Page
from ptext.object.event_listener import EventListener
from ptext.primitive.pdf_dictionary import PDFDictionary
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.types_with_parent_attribute import (
    DictionaryWithParentAttribute,
    ListWithParentAttribute,
)


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
    ) -> Any:

        # convert dictionary like structure
        tmp = Page().set_parent(parent_object)

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
                tmp[k.name] = v

        # send out BeginPageEvent
        tmp.event_occurred(BeginPageEvent(tmp))

        # set up canvas
        if "Contents" not in tmp:
            raise PDFTypeError(
                expected_type=Union[
                    ListWithParentAttribute, DictionaryWithParentAttribute
                ],
                received_type=None,
            )
        contents = tmp["Contents"]
        if contents != PDFNull():
            canvas = Canvas().set_parent(tmp)

            # process bytes in stream
            if isinstance(contents, dict):
                canvas.read(io.BytesIO(contents["DecodedBytes"]))

            # process bytes in array
            if isinstance(contents, list):
                bts = b"".join([x["DecodedBytes"] + b" " for x in contents])
                canvas.read(io.BytesIO(bts))

        # send out EndPageEvent
        tmp.event_occurred(EndPageEvent(tmp))

        # return
        return tmp
