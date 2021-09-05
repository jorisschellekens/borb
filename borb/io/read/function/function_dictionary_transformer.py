#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a Function Dictionary
"""
import io
import typing
from decimal import Decimal
from typing import Any, Optional, Union

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.transformer import Transformer, ReadTransformerState
from borb.io.read.types import AnyPDFType, Dictionary, Function, Name, Reference, Stream
from borb.pdf.canvas.event.event_listener import EventListener


class FunctionDictionaryTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a Function Dictionary
    """

    def __init__(self):
        super(FunctionDictionaryTransformer, self).__init__()

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed is a Dictionary with \FunctionType key
        """
        return (
            isinstance(object, dict)
            and "FunctionType" in object
            and isinstance(object["FunctionType"], Decimal)
            and int(object["FunctionType"]) in [0, 2, 3, 4]
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a Dictionary with \FunctionType key from a byte stream.
        """
        assert isinstance(object_to_transform, Dictionary)
        assert "FunctionType" in object_to_transform
        assert isinstance(object_to_transform["FunctionType"], Decimal)

        function_type: int = int(object_to_transform["FunctionType"])
        assert function_type in [0, 2, 3, 4], "FunctionType must be in [0, 2, 3, 4]"

        transformed_object: Function = Function()

        if isinstance(object_to_transform, Stream):
            decode_stream(object_to_transform)
            transformed_object[Name("Bytes")] = object_to_transform["Bytes"]
            transformed_object[Name("DecodedBytes")] = object_to_transform[
                "DecodedBytes"
            ]

        # add listener(s)
        for l in event_listeners:
            transformed_object.add_event_listener(l)  # type: ignore [attr-defined]

        # resolve references in stream dictionary
        assert context is not None
        assert context.tokenizer is not None
        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.items():
            if isinstance(v, Reference):
                v = xref.get_object(v, context.source, context.tokenizer)
                transformed_object[k] = v

        # convert (remainder of) stream dictionary
        for k, v in object_to_transform.items():
            if not isinstance(v, Reference):
                v = self.get_root_transformer().transform(
                    v, transformed_object, context, []
                )
                if v is not None:
                    transformed_object[k] = v

        # linkage
        transformed_object.set_parent(parent_object)  # type: ignore [attr-defined]

        # return
        return transformed_object
