#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or persistence of integer objects within the PDF structure.

This class is designed to traverse and process nodes containing integer data in the PDF
document tree. It ensures that integer values are correctly written and formatted according
to PDF standards, allowing for proper storage and representation within the document.
"""
import typing

from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class IntVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or persistence of integer objects within the PDF structure.

    This class is designed to traverse and process nodes containing integer data in the PDF
    document tree. It ensures that integer values are correctly written and formatted according
    to PDF standards, allowing for proper storage and representation within the document.
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
        if not isinstance(node, int):
            return False

        # default
        self._append_bytes_or_str(str(node))
        return True
