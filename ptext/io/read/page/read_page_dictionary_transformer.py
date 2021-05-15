#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of ReadBaseTransformer is responsible for reading Page objects
"""
import io
import typing
from typing import Optional, Any, Union, Dict

from ptext.io.read.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read.types import (
    Dictionary,
    AnyPDFType,
)
from ptext.pdf.canvas.canvas import Canvas
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.end_page_event import EndPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.pdf.page.page import Page


class ReadPageDictionaryTransformer(ReadBaseTransformer):
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
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a \Page Dictionary from a byte stream
        """

        if isinstance(object_to_transform, Page):
            return object_to_transform

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
        tmp._event_occurred(BeginPageEvent(tmp))

        # set up canvas
        assert "Contents" in tmp
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
        tmp._event_occurred(EndPageEvent(tmp))

        # return
        return tmp
