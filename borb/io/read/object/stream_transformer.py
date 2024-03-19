#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading Stream objects
"""
import io
import typing

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.pdf.canvas.event.event_listener import EventListener


class StreamTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading Stream objects
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
        This function returns True if the object to be transformed is a Stream
        :param object:  the object to be transformed
        :return:        True if the object is a Stream, False otherwise
        """
        return isinstance(object, Stream)

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms a PDF Stream
        :param object_to_transform:     the Stream to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        a Stream Object
        """
        assert isinstance(object_to_transform, Stream)
        object_to_transform.set_parent(parent_object)

        # resolve references in stream dictionary
        # fmt: off
        assert context is not None, "context must be defined to read Stream objects"
        assert (context.tokenizer is not None), "context.tokenizer must be defined to read Stream objects"
        # fmt: on

        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.items():
            if isinstance(v, Reference):
                v = xref.get_object(v, context.source, context.tokenizer)
                object_to_transform[k] = v

        # IF context.security_handler is present
        # THEN apply decryption
        if context.security_handler is not None:
            object_to_transform = context.security_handler.decrypt(object_to_transform)

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
        object_to_transform.set_parent(parent_object)

        # return
        return object_to_transform
