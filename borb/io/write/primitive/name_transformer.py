#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Name objects
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Name
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState


class NameTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Name objects
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
        This function returns True if the object to be transformed is a Name
        :param object:  the object to be transformed
        :return:        True if the object is a Name, False otherwise
        """
        return isinstance(object, Name)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a Name Object into a byte stream
        :param object_to_transform:     the Name Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Name Object
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Name)

        context.destination.write(bytes("/" + str(object_to_transform), "latin1"))
