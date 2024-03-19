#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing String objects
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import HexadecimalString
from borb.io.read.types import String
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState


class StringTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing String objects
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

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is a String
        :param object:  the object to be transformed
        :return:        True if the object is a String (or HexadecimalString), False otherwise
        """
        return isinstance(object, String) or isinstance(object, HexadecimalString)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a String Object into a byte stream
        :param object_to_transform:     the String Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) String Object
        """
        assert (
            context is not None
        ), "A WriteTransformerState must be defined in order to write String objects."
        assert context.destination is not None
        assert isinstance(object_to_transform, String)

        if isinstance(object_to_transform, HexadecimalString):
            context.destination.write(
                bytes("<" + str(object_to_transform) + ">", "latin1")
            )
            return

        if isinstance(object_to_transform, String):
            context.destination.write(
                bytes("(" + str(object_to_transform) + ")", "latin1")
            )
            return
