#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Decimal objects
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState


class NumberTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Decimal objects
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
        This function returns True if the object to be transformed is a Decimal
        :param object:  the object to be transformed
        :return:        True if the object is a Decimal, False otherwise
        """
        return isinstance(object, Decimal)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a Decimal Object into a byte stream
        :param object_to_transform:     the Decimal Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Decimal Object
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Decimal)

        is_integer = object_to_transform == int(object_to_transform)

        if is_integer:
            context.destination.write(bytes(str(int(object_to_transform)), "latin1"))
        else:
            context.destination.write(
                bytes("{:.2f}".format(float(object_to_transform)), "latin1")
            )
