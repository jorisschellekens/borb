#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing booleans
"""
from typing import Optional

from borb.io.read.types import AnyPDFType, Boolean
from borb.io.write.transformer import Transformer, WriteTransformerState


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

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents a Boolean object
        """
        return isinstance(any, Boolean)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes a Boolean to a byte stream
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
