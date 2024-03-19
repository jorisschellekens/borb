#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing References
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Reference
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState


class ReferenceTransform(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing References
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
        This function returns True if the object to be transformed is a Reference
        :param object:  the object to be transformed
        :return:        True if the object is a Reference, False otherwise
        """
        return isinstance(object, Reference)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a Reference Object into a byte stream
        :param object_to_transform:     the Reference Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Reference Object
        """
        assert (
            context is not None
        ), "A WriteTransformerState must be defined in order to write Reference objects."
        assert context.destination is not None
        assert isinstance(object_to_transform, Reference)

        assert object_to_transform.object_number is not None
        context.destination.write(
            bytes(
                "%d %d R"
                % (
                    object_to_transform.object_number,
                    object_to_transform.generation_number or 0,
                ),
                "latin1",
            )
        )
