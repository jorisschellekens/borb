#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing String objects
"""
from typing import Optional

from borb.io.read.types import AnyPDFType, HexadecimalString, String
from borb.io.write.transformer import Transformer, WriteTransformerState


class StringTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing String objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents a String or HexadecimalString
        """
        return isinstance(any, String) or isinstance(any, HexadecimalString)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes a String object to a byte stream
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
