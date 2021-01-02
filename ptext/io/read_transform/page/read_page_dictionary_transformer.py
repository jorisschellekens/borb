import io
import typing
from typing import Optional, List, Any, Union, Dict

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    TransformerContext,
)
from ptext.io.read_transform.types import (
    Dictionary,
    List,
    AnyPDFType,
)
from ptext.pdf.canvas.canvas import Canvas
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.end_page_event import EndPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.pdf.page.page import Page


class ReadPageDictionaryTransformer(ReadBaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Dict) and "Type" in object and object["Type"] == "Page"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # convert dictionary like structure
        tmp = Page().set_parent(parent_object)  # type: ignore [attr-defined]

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)  # type: ignore [attr-defined]

        # convert key/value pairs
        assert isinstance(object_to_transform, Dictionary)
        for k, v in object_to_transform.items():
            # avoid circular reference
            if k == "Parent":
                continue
            v = self.get_root_transformer().transform(v, tmp, context, [])
            if v is not None:
                tmp[k] = v

        # send out BeginPageEvent
        tmp.event_occurred(BeginPageEvent(tmp))

        # set up canvas
        if "Contents" not in tmp:
            raise PDFTypeError(
                expected_type=Union[List, Dictionary],
                received_type=None,
            )
        contents = tmp["Contents"]
        if contents is not None:
            canvas = Canvas().set_parent(tmp)  # type: ignore [attr-defined]

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
