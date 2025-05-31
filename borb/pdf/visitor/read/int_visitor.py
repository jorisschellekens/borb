#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing integer values from a PDF byte stream.

`IntVisitor` is a specialized visitor that identifies and processes integer values
within a PDF structure, converting byte sequences representing integers into
Python `int` objects. This class extends `ReadVisitor` to support traversing nodes
in a PDF document tree using the visitor pattern, isolating integer-specific
handling logic.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class IntVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing integer values from a PDF byte stream.

    `IntVisitor` is a specialized visitor that identifies and processes integer values
    within a PDF structure, converting byte sequences representing integers into
    Python `int` objects. This class extends `ReadVisitor` to support traversing nodes
    in a PDF document tree using the visitor pattern, isolating integer-specific
    handling logic.
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
        if self.get_bytes()[node] not in b"-0123456789":
            return None

        i: int = node
        j: int = node
        if self.get_bytes()[j : j + 1] == b"-":
            j += 1
        while self.get_bytes()[j] in b"0123456789":
            j += 1

        return int(self.get_bytes()[i:j]), j
