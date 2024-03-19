#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a Function Dictionary
"""
import io
import typing
from decimal import Decimal

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Dictionary
from borb.io.read.types import Function
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.pdf.canvas.event.event_listener import EventListener


class FunctionDictionaryTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a Function Dictionary
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(
        self,
        object: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType],
    ) -> bool:
        """
        This function returns True if the object to be transformed is a Dictionary with /FunctionType key
        :param object:  the object to be transformed
        :return:        True if the object is a FunctionType Dictionary, False otherwise
        """
        return (
            isinstance(object, dict)
            and "FunctionType" in object
            and isinstance(object["FunctionType"], Decimal)
            and int(object["FunctionType"]) in [0, 2, 3, 4]
        )

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms a FunctionType Dictionary into a Function Object
        :param object_to_transform:     the FunctionType Dictionary to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        a Function Object
        """
        # fmt: off
        assert isinstance(object_to_transform, Dictionary), "object_to_transform must be of type Dictionary."
        assert "FunctionType" in object_to_transform, "object_to_transform Dictionary must be FunctionType."
        assert isinstance(object_to_transform["FunctionType"], Decimal), "object_to_transform must contain a valid /FunctionType entry."
        # fmt: on

        function_type: int = int(object_to_transform["FunctionType"])
        assert function_type in [0, 2, 3, 4], "FunctionType must be in [0, 2, 3, 4]"

        transformed_object: Function = Function()

        if isinstance(object_to_transform, Stream):
            # fmt: off
            decode_stream(object_to_transform)
            transformed_object[Name("Bytes")] = object_to_transform["Bytes"]
            transformed_object[Name("DecodedBytes")] = object_to_transform["DecodedBytes"]
            # fmt: on

        # resolve references in stream dictionary
        # fmt: off
        assert (context is not None), "context must be defined to read (Function) Dictionary objects"
        assert (context.tokenizer is not None), "context.tokenizer must be defined to read (Function) Dictionary objects"
        # fmt: on
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
        transformed_object.set_parent(parent_object)

        # return
        return transformed_object
