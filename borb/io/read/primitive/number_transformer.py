#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading Decimal objects
"""
import io
import typing
from typing import Any, Optional, Union

from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, Decimal
from borb.pdf.canvas.event.event_listener import EventListener


class NumberTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading Decimal objects
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed is a Decimal object
        """
        return isinstance(object, Decimal)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a Decimal from a byte stream
        """
        assert isinstance(object_to_transform, Decimal)
        return Decimal(object_to_transform).set_parent(parent_object)  # type: ignore [attr-defined]
