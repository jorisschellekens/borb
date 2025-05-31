#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing list structures in a PDF byte stream.

`ListVisitor` extends `ReadVisitor` to identify and process list structures
within a PDF, specifically targeting arrays of values as defined by the PDF
specification. Using the visitor pattern, `ListVisitor` traverses nodes in
the PDF document tree, converting recognized list structures into corresponding
Python lists, with each element processed and converted based on its type.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class ListVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing list structures in a PDF byte stream.

    `ListVisitor` extends `ReadVisitor` to identify and process list structures
    within a PDF, specifically targeting arrays of values as defined by the PDF
    specification. Using the visitor pattern, `ListVisitor` traverses nodes in
    the PDF document tree, converting recognized list structures into corresponding
    Python lists, with each element processed and converted based on its type.
    """

    __LIST_CLOSE_BRACKETS = b"]"
    __LIST_OPEN_BRACKETS = b"["
    __SPACE = b" "

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
        if self.get_bytes()[node : node + 1] != ListVisitor.__LIST_OPEN_BRACKETS:
            return None

        retval: typing.List[PDFType] = []
        i: int = node + 1
        while i < len(self.get_bytes()):

            # keep track of depth of list
            if self.get_bytes()[i : i + 1] == ListVisitor.__LIST_CLOSE_BRACKETS:
                i += 1
                break

            # read a space
            if self.get_bytes()[i : i + 1] == ListVisitor.__SPACE:
                i += 1
                continue

            # IF we see a newline (\n\r)
            # THEN skip
            if self.get_bytes()[i : i + 2] == b"\n\r":
                i += 2
                continue
            if self.get_bytes()[i : i + 2] == b"\r\n":
                i += 2
                continue
            if self.get_bytes()[i : i + 1] == b"\n":
                i += 1
                continue
            if self.get_bytes()[i : i + 1] == b"\r":
                i += 1
                continue

            val_and_i = self.root_generic_visit(i)
            assert val_and_i is not None
            val, i = val_and_i
            retval += [val]

        # return
        return retval, i
