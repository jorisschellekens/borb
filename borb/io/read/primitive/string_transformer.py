#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading String objects
"""
import io
import typing

from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import HexadecimalString
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.event.event_listener import EventListener


class StringTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading String objects
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
        This function returns True if the object to be transformed is a string
        :param object:  the object to be transformed
        :return:        True if the object is a string, False otherwise
        """
        return (
            isinstance(object, String)
            or isinstance(object, HexadecimalString)
            or isinstance(object, Name)
        )

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms a PDF string into a (borb) Python String
        :param object_to_transform:     the string to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        a String Object
        """

        # set parent
        assert (
            isinstance(object_to_transform, String)
            or isinstance(object_to_transform, HexadecimalString)
            or isinstance(object_to_transform, Name)
        )
        object_to_transform.set_parent(parent_object)
        return object_to_transform
        # return
