#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTransformer converts a PDFArray to a List
"""
import io
import typing
from typing import Union, Any, Optional

from ptext.io.read.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read.types import List, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadArrayTransformer(ReadBaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFArray to a List
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        return isinstance(object, List)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # create root object
        assert isinstance(object_to_transform, List)
        object_to_transform.set_parent(parent_object)  # type: ignore [attr-defined]

        # add listener(s)
        for l in event_listeners:
            object_to_transform.add_event_listener(l)  # type: ignore [attr-defined]

        # transform child(ren)
        for i in range(0, len(object_to_transform)):
            object_to_transform[i] = self.get_root_transformer().transform(
                object_to_transform[i], object_to_transform, context, []
            )

        # return
        return object_to_transform
