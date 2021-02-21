#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of ReadBaseTransformer is responsible for reading Decimal objects
"""
import io
import typing
from typing import Optional, Any, Union

from ptext.io.read.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read.types import Decimal, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadNumberTransformer(ReadBaseTransformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading Decimal objects
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        return isinstance(object, Decimal)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        assert isinstance(object_to_transform, Decimal)
        return Decimal(object_to_transform).set_parent(parent_object)  # type: ignore [attr-defined]
