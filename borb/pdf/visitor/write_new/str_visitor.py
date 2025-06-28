#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or processing of string objects within the PDF structure.

The `StrVisitor` class is responsible for traversing and processing nodes that contain string
values in the PDF document tree. It ensures that string objects are correctly written or exported,
handling the necessary formatting, encoding, and any specific PDF string-related requirements.

This class inherits from the `WriteNewVisitor` class and focuses on processing string nodes in a
manner consistent with the PDF standard.
"""
import typing

from borb.pdf.primitives import name
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class StrVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or processing of string objects within the PDF structure.

    The `StrVisitor` class is responsible for traversing and processing nodes that contain string
    values in the PDF document tree. It ensures that string objects are correctly written or exported,
    handling the necessary formatting, encoding, and any specific PDF string-related requirements.

    This class inherits from the `WriteNewVisitor` class and focuses on processing string nodes in a
    manner consistent with the PDF standard.
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

    def visit(self, node: typing.Any) -> bool:
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
        if not isinstance(node, str):
            return False

        # name
        if isinstance(node, name):
            self._append_bytes_or_str(f"/{node}")
            return True

        # default
        self._append_bytes_or_str(f"({node})")
        return True
