#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of WriteBaseTransformer is responsible for writing String objects
"""
from typing import Optional

from ptext.io.read.types import AnyPDFType, HexadecimalString, String
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteStringTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing String objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, String) or isinstance(any, HexadecimalString)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        """
        This method writes a String object to a byte stream
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, str)

        if isinstance(object_to_transform, HexadecimalString):
            context.destination.write(bytes("<" + object_to_transform + ">", "latin1"))
            return

        if isinstance(object_to_transform, String):
            context.destination.write(bytes("(" + object_to_transform + ")", "latin1"))
            return
