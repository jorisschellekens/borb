#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or persistence of `float` objects in the PDF structure.

This class is designed to traverse and process nodes containing `float` data within the
PDF document structure. It extends the functionality of `WriteNewVisitor` by providing
specific methods to handle the writing of floating-point values, ensuring proper formatting
and storage within the PDF.
"""
import typing

from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class FloatVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or persistence of `float` objects in the PDF structure.

    This class is designed to traverse and process nodes containing `float` data within the
    PDF document structure. It extends the functionality of `WriteNewVisitor` by providing
    specific methods to handle the writing of floating-point values, ensuring proper formatting
    and storage within the PDF.
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
        if not isinstance(node, float):
            return False

        # default
        self._append_bytes_or_str(str(round(node, 7)))
        return True
