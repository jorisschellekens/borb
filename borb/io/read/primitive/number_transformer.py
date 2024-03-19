#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading Decimal objects
"""
import io
import typing

from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.pdf.canvas.event.event_listener import EventListener


class NumberTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading Decimal objects
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
        This function returns True if the object to be transformed is a number
        :param object:  the object to be transformed
        :return:        True if the object is a number, False otherwise
        """
        return isinstance(object, bDecimal)

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms a PDF number into a (borb) Python Decimal
        :param object_to_transform:     the number to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        a Decimal Object
        """

        # fmt: off
        assert isinstance(object_to_transform, bDecimal), "object_to_transform must be of type Decimal"
        return bDecimal(object_to_transform).set_parent(parent_object)
        # fmt: on
