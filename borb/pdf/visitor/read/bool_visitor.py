#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and interpreting boolean values in a PDF byte stream.

`BoolVisitor` is a specialized `ReadVisitor` used to identify and process boolean
literals ("true" and "false") within a PDF document, following the PDF specification.
Using the visitor pattern, this class traverses nodes in the PDF document tree and
converts recognized boolean structures into Python `True` or `False` values.

The `generic_visit` method performs the core logic of identifying these boolean values
by checking for the presence of "true" or "false" in the PDF's byte stream at a given
position, allowing for efficient parsing of boolean data.

This class contributes to PDF parsing by enabling the extraction of boolean data types,
which are fundamental in defining conditions, attributes, and flags within PDF dictionaries
and objects.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class BoolVisitor(ReadVisitor):
    """
    Visitor class for reading and interpreting boolean values in a PDF byte stream.

    `BoolVisitor` is a specialized `ReadVisitor` used to identify and process boolean
    literals ("true" and "false") within a PDF document, following the PDF specification.
    Using the visitor pattern, this class traverses nodes in the PDF document tree and
    converts recognized boolean structures into Python `True` or `False` values.

    The `generic_visit` method performs the core logic of identifying these boolean values
    by checking for the presence of "true" or "false" in the PDF's byte stream at a given
    position, allowing for efficient parsing of boolean data.

    This class contributes to PDF parsing by enabling the extraction of boolean data types,
    which are fundamental in defining conditions, attributes, and flags within PDF dictionaries
    and objects.
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

    def visit(
        self, node: typing.Union[int, PDFType]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
        """
        Traverse the PDF document tree using the visitor pattern.

        This method is called when a node does not have a specialized handler.
        Subclasses can override this method to provide default behavior or logging
        for unsupported nodes. If any operation is performed on the node (e.g.,
        writing or persisting), the method returns `True`. Otherwise, it returns
        `False` to indicate that the visitor did not process the node.

        :param node:    the node (PDFType) to be processed
        :return:        True if the visitor processed the node False otherwise
        """
        if not isinstance(node, int):
            return None
        if self.get_bytes()[node : node + 4] == b"true":
            return True, node + 4
        if self.get_bytes()[node : node + 5] == b"false":
            return False, node + 5
        return None
