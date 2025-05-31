#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A `ReferenceVisitor` implementation that skips reference lookups during PDF processing.

The `NoOpReferenceVisitor` is a specialized visitor class used when processing object streams
in a PDF. Unlike the standard `ReferenceVisitor`, it does not attempt to resolve references
to other objects within the PDF file. This behavior is necessary when handling object streams
because the references embedded within these streams can only be resolved later, outside the
immediate context of the bytes inside the stream.

This class is particularly useful in situations where resolving references prematurely may
lead to errors or incorrect behavior, such as when parsing incremental updates or deferred
content in PDFs.
"""
import typing

from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class NoOpReferenceVisitor(ReadVisitor):
    """
    A `ReferenceVisitor` implementation that skips reference lookups during PDF processing.

    The `NoOpReferenceVisitor` is a specialized visitor class used when processing object streams
    in a PDF. Unlike the standard `ReferenceVisitor`, it does not attempt to resolve references
    to other objects within the PDF file. This behavior is necessary when handling object streams
    because the references embedded within these streams can only be resolved later, outside the
    immediate context of the bytes inside the stream.

    This class is particularly useful in situations where resolving references prematurely may
    lead to errors or incorrect behavior, such as when parsing incremental updates or deferred
    content in PDFs.
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
        if self.get_bytes()[node] not in b"0123456789":
            return None

        # read object nr
        i: int = node
        j: int = node
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        object_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read generation number
        i = j
        if self.get_bytes()[i] not in b"0123456789":
            return None
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        generation_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read 'R'
        i = j
        if self.get_bytes()[i : i + 1] != b"R":
            return None
        i += 1

        return reference(object_nr=object_nr, generation_nr=generation_nr), i
