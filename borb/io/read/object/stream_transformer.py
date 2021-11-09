#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading Stream objects
"""
import io
import typing
from typing import Any, Optional, Union

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, Reference, Stream
from borb.pdf.canvas.event.event_listener import EventListener


class StreamTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading Stream objects
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be converted represents a Stream object
        """
        return isinstance(object, Stream)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a Stream from a byte stream
        """
        assert isinstance(object_to_transform, Stream)
        object_to_transform.set_parent(parent_object)  # type: ignore [attr-defined]

        # resolve references in stream dictionary
        assert context is not None
        assert context.tokenizer is not None
        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.items():
            if isinstance(v, Reference):
                v = xref.get_object(v, context.source, context.tokenizer)
                object_to_transform[k] = v

        # apply filter(s)
        object_to_transform = decode_stream(object_to_transform)

        # convert (remainder of) stream dictionary
        for k, v in object_to_transform.items():
            if not isinstance(v, Reference):
                v = self.get_root_transformer().transform(
                    v, object_to_transform, context, []
                )
                if v is not None:
                    object_to_transform[k] = v

        # linkage
        object_to_transform.set_parent(parent_object)  # type: ignore [attr-defined]

        # return
        return object_to_transform
