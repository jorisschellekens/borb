#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing name objects in a PDF byte stream.

`NameVisitor` extends `ReadVisitor` to identify and process name objects within
a PDF, converting these into corresponding Python strings. Using the visitor pattern,
`NameVisitor` traverses PDF nodes and extracts name objects according to the PDF
specification, facilitating structured parsing of named resources and keys.
"""
import typing

from borb.pdf.primitives import PDFType, name
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class NameVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing name objects in a PDF byte stream.

    `NameVisitor` extends `ReadVisitor` to identify and process name objects within
    a PDF, converting these into corresponding Python strings. Using the visitor pattern,
    `NameVisitor` traverses PDF nodes and extracts name objects according to the PDF
    specification, facilitating structured parsing of named resources and keys.
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
        if self.get_bytes()[node : node + 1] != b"/":
            return None

        # find
        i: int = node
        j: int = node + 1
        while self.get_bytes()[j] not in b"()<>[]{}/%\x00\x09\x0a\x0c\x0d\x20":
            j += 1

        # return
        return name(self.get_bytes()[i + 1 : j].decode()), j
