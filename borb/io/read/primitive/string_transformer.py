#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading String objects
"""
import io
import typing
from typing import Any, Optional, Union

from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, HexadecimalString, Name, String
from borb.pdf.canvas.event.event_listener import EventListener


class StringTransformer(Transformer):
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
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a String from a byte stream
        """
        # set parent
        object_to_transform.set_parent(parent_object)  # type: ignore[union-attr]
        # return
        return object_to_transform
