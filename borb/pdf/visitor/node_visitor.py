#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract base class for implementing the Visitor pattern in PDF structure traversal.

The `NodeVisitor` class serves as a superclass for various concrete visitor
implementations that traverse the PDF document structure. This class defines
the interface and common functionality for visitors, enabling them to process
different types of nodes (e.g., pages, images, text) within the PDF hierarchy.
By utilizing the Visitor pattern, this design promotes separation of concerns,
allowing for operations such as reading, writing, or manipulating the PDF content
without modifying the node classes themselves.
"""
import typing


class NodeVisitor:
    """
    Abstract base class for implementing the Visitor pattern in PDF structure traversal.

    The `NodeVisitor` class serves as a superclass for various concrete visitor
    implementations that traverse the PDF document structure. This class defines
    the interface and common functionality for visitors, enabling them to process
    different types of nodes (e.g., pages, images, text) within the PDF hierarchy.
    By utilizing the Visitor pattern, this design promotes separation of concerns,
    allowing for operations such as reading, writing, or manipulating the PDF content
    without modifying the node classes themselves.
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

    def visit(self, node: typing.Any) -> typing.Optional[typing.Any]:
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
        return False
