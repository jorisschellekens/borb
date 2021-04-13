#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of ReadBaseTransformer is responsible for reading String objects
"""
import io
import typing
from typing import Optional, Any, Union

from ptext.io.read.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read.types import (
    String,
    HexadecimalString,
    Name,
    AnyPDFType,
)
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadStringTransformer(ReadBaseTransformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading String objects
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be converted represents a String or Hexadecimal String or a Name
        """
        return (
            isinstance(object, String)
            or isinstance(object, HexadecimalString)
            or isinstance(object, Name)
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function writes a String to a byte stream
        """
        # set parent
        object_to_transform.set_parent(parent_object)  # type: ignore[union-attr]
        # return
        return object_to_transform
