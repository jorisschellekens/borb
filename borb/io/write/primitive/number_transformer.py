#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Decimal objects
"""
from typing import Optional

from borb.io.read.types import AnyPDFType, Decimal
from borb.io.write.transformer import Transformer, WriteTransformerState


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

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents a Decimal object
        """
        return isinstance(any, Decimal)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes a Decimal to a byte stream
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
