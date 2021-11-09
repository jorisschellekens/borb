#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading Page objects
"""
import io
import typing
import zlib
from typing import Any, Dict, Optional, Union

from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as pDecimal
from borb.io.read.types import Dictionary, List, Name, Stream
from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.page.page import Page


class PageDictionaryTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading Page objects
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be converted represents a \Page Dictionary
        """
        return (
            isinstance(object, Dict) and "Type" in object and object["Type"] == "Page"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a \Page Dictionary from a byte stream
        """

        if isinstance(object_to_transform, Page):
            return object_to_transform

        # convert dictionary like structure
        page_out = Page().set_parent(parent_object)  # type: ignore [attr-defined]

        # convert key/value pairs
        assert isinstance(object_to_transform, Dictionary)
        for k, v in object_to_transform.items():
            # avoid circular reference
            if k == "Parent":
                continue
            v = self.get_root_transformer().transform(
                v, page_out, context, event_listeners
            )
            if v is not None:
                page_out[k] = v

        # send out BeginPageEvent
        for l in event_listeners:
            l._event_occurred(BeginPageEvent(page_out))

        # check whether `Contents` exists
        if "Contents" not in page_out:
            return
        if not isinstance(page_out["Contents"], List) and not isinstance(
            page_out["Contents"], Stream
        ):
            return

        # Force content to be Stream (rather than List)
        contents = page_out["Contents"]
        if isinstance(contents, List):
            bts = b"".join([x["DecodedBytes"] + b" " for x in contents])
            page_out[Name("Contents")] = Stream()
            assert isinstance(page_out["Contents"], Stream)
            page_out["Contents"][Name("DecodedBytes")] = bts
            page_out["Contents"][Name("Bytes")] = zlib.compress(bts, 9)
            page_out["Contents"][Name("Filter")] = Name("FlateDecode")
            page_out["Contents"][Name("Length")] = pDecimal(len(bts))
            contents = page_out["Contents"]
            contents.set_parent(page_out)  # type: ignore [attr-defined]

        # create Canvas
        canvas = Canvas().set_parent(page_out)  # type: ignore [attr-defined]

        # If there are no event listeners, processing the page has no effect
        # we may as well skip it (cause it is very labour-intensive).
        if len(event_listeners) > 0:
            # create CanvasStreamProcessor
            CanvasStreamProcessor(page_out, canvas, []).read(
                io.BytesIO(contents["DecodedBytes"]), event_listeners
            )

        # send out EndPageEvent
        for l in event_listeners:
            l._event_occurred(EndPageEvent(page_out))

        # return
        return page_out
