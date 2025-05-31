#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing string objects in a PDF byte stream.

`HexStrVisitor` extends `ReadVisitor` to identify and process string objects
within a PDF, converting them into Python strings. Using the visitor pattern,
`HexStrVisitor` traverses PDF nodes, extracting and decoding string values
according to the PDF specification, allowing for structured handling of
text content in the document.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class HexStrVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing string objects in a PDF byte stream.

    `HexStrVisitor` extends `ReadVisitor` to identify and process string objects
    within a PDF, converting them into Python strings. Using the visitor pattern,
    `HexStrVisitor` traverses PDF nodes, extracting and decoding string values
    according to the PDF specification, allowing for structured handling of
    text content in the document.
    """

    __STR_CLOSE_BRACKET = b">"
    __STR_OPEN_BRACKET = b"<"

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
        if self.get_bytes()[node : node + 1] != HexStrVisitor.__STR_OPEN_BRACKET:
            return None

        i: int = node
        j: int = self.get_bytes().find(HexStrVisitor.__STR_CLOSE_BRACKET, node)
        if any(
            [x not in b"0123456789abcdefABCDEF" for x in self.get_bytes()[i + 1 : j]]
        ):
            return None

        # return
        return self.get_bytes()[i + 1 : j].decode(), j + 1
