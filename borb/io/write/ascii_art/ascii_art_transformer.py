#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing ASCII art in every PDF
"""
from pathlib import Path
from typing import Optional

from borb.io.read.types import AnyPDFType, Stream
from borb.io.write.transformer import (
    Transformer,
    WriteTransformerState,
)


class ASCIIArtTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing ASCII art in every PDF
    """

    def __init__(self):
        super().__init__()
        self._has_been_used: bool = False

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True once per Document (on the first Stream object) and embeds some ASCII art
        This is used to embed the current version in each Document
        """
        return isinstance(any, Stream) and not self._has_been_used

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes ASCII art to a byte stream
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Stream)

        f = Path(__file__).parent / "ascii_logo.txt"
        with open(f, "r") as logo_file_handle:
            ascii_logo = logo_file_handle.readlines()

        # append newline (if needed)
        if ascii_logo[-1][-1] != "\n":
            ascii_logo[-1] += "\n"

        # convert to latin1
        ascii_logo_bytes = [bytes("%    " + x, "utf8") for x in ascii_logo]

        self._has_been_used = True
        for x in ascii_logo_bytes:
            context.destination.write(x)
        context.destination.write(bytes("\n", "utf8"))

        self.get_root_transformer().transform(object_to_transform, context)
