#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing booleans
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Boolean
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState


class BooleanTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing booleans
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
        This function returns True if the object to be transformed is a Boolean
        :param object:  the object to be transformed
        :return:        True if the object is a Boolean, False otherwise
        """
        return isinstance(object, Boolean)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a Boolean Object into a byte stream
        :param object_to_transform:     the Boolean Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Boolean Object
        """
        # fmt: off
        assert context is not None, "context must be defined to write bool objects"
        assert context.destination is not None, "context.destination must be defined to write bool objects"
        assert isinstance(object_to_transform, Boolean), "object_to_transform must be of type Boolean"
        # fmt: on

        if bool(object_to_transform):
            context.destination.write(bytes("true", "latin1"))
        else:
            context.destination.write(bytes("false", "latin1"))
