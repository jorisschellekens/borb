#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing floating-point numbers in a PDF byte stream.

The `FloatVisitor` class extends `ReadVisitor` and is specialized in identifying and
processing floating-point numbers within a PDF. Floating-point numbers in PDF syntax
represent values with decimal points, which are often used to define coordinates, dimensions,
and other measurements.

The class uses the visitor pattern to traverse the PDF document structure, locating
byte sequences that represent floating-point values and converting them into native Python
`float` objects for further processing. This allows for accurate interpretation of
measurements and other numerical data in a PDF document.
"""

import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class FloatVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing floating-point numbers in a PDF byte stream.

    The `FloatVisitor` class extends `ReadVisitor` and is specialized in identifying and
    processing floating-point numbers within a PDF. Floating-point numbers in PDF syntax
    represent values with decimal points, which are often used to define coordinates, dimensions,
    and other measurements.

    The class uses the visitor pattern to traverse the PDF document structure, locating
    byte sequences that represent floating-point values and converting them into native Python
    `float` objects for further processing. This allows for accurate interpretation of
    measurements and other numerical data in a PDF document.
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
        if self.get_bytes()[node] not in b"-.0123456789":
            return None

        i: int = node
        j: int = node
        if self.get_bytes()[j : j + 1] == b"-":
            j += 1

        # process any number of leading digits
        has_seen_leading_digits: bool = False
        while self.get_bytes()[j] in b"0123456789":
            has_seen_leading_digits = True
            j += 1

        # process period
        has_seen_period: bool = False
        if self.get_bytes()[j : j + 1] == b".":
            has_seen_period = True
            j += 1

        # process any number of trailing digits
        has_seen_trailing_digits: bool = False
        while self.get_bytes()[j] in b"0123456789":
            has_seen_trailing_digits = True
            j += 1

        if not has_seen_period:
            return None
        if not (has_seen_leading_digits or has_seen_trailing_digits):
            return None

        return float(self.get_bytes()[i:j]), j
