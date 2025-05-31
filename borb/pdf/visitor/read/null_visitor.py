#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling null objects in a PDF.

The `NullVisitor` is responsible for reading and processing null objects (`null`)
within a PDF. Null objects are a core data type in the PDF specification, representing
the absence of a value.

This class ensures that null objects are correctly identified and handled during
the parsing of a PDF file, allowing for consistent treatment of these objects
within the document's data structure.
"""

import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class NullVisitor(ReadVisitor):
    """
    A visitor class for handling null objects in a PDF.

    The `NullVisitor` is responsible for reading and processing null objects (`null`)
    within a PDF. Null objects are a core data type in the PDF specification, representing
    the absence of a value.

    This class ensures that null objects are correctly identified and handled during
    the parsing of a PDF file, allowing for consistent treatment of these objects
    within the document's data structure.
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
        if self.get_bytes()[node : node + 4] != b"null":
            return None

        # return
        return (None, node + 4)  # type: ignore[return-value]
