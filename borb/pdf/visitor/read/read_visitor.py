#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and processing PDF nodes.

`ReadVisitor` is a subclass of `NodeVisitor` that provides functionality
for visiting and processing PDF nodes. It works within the visitor pattern
and is designed to interact with the root visitor (`FacadeVisitor`) to
traverse and process different parts of a PDF document.

This class serves as a generic visitor that can be used to handle reading
operations on PDF nodes, delegating the actual logic to the root visitor
and simplifying the management of PDF traversal.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.node_visitor import NodeVisitor


class ReadVisitor(NodeVisitor):
    """
    Visitor class for reading and processing PDF nodes.

    `ReadVisitor` is a subclass of `NodeVisitor` that provides functionality
    for visiting and processing PDF nodes. It works within the visitor pattern
    and is designed to interact with the root visitor (`FacadeVisitor`) to
    traverse and process different parts of a PDF document.

    This class serves as a generic visitor that can be used to handle reading
    operations on PDF nodes, delegating the actual logic to the root visitor
    and simplifying the management of PDF traversal.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, root: typing.Optional[NodeVisitor] = None) -> None:
        """
        Initialize a ReadVisitor instance.

        This constructor initializes the `ReadVisitor` class, which is a visitor
        for processing PDF nodes. The visitor may optionally be given a reference
        to a root visitor (`FacadeVisitor`) to delegate the processing of PDF nodes.
        The root visitor serves as the main controller for node traversal, and this
        class allows for interaction with that root instance.

        :param root: An optional reference to the root visitor (`FacadeVisitor`)
                     which will be used to delegate the visiting of PDF nodes.
        """
        super().__init__()
        self.__root: typing.Optional[NodeVisitor] = root

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_bytes(self) -> bytes:
        """
        Retrieve the raw PDF byte data being processed.

        This method returns the PDF byte data that the root visitor (`FacadeVisitor`)
        is currently processing. The byte data is stored and managed by the root visitor
        and can be accessed through this method. It allows subclasses of `ReadVisitor`
        to access the PDF content for further processing or analysis.

        :return: The raw PDF byte data as a `bytes` object.
        """
        assert self.__root is not None
        return self.__root._RootVisitor__source  # type: ignore[attr-defined]

    def root_generic_visit(
        self, node: typing.Union[bytes, int]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
        """
        Delegate the visiting of a PDF node to the root visitor.

        This method checks if a root visitor instance is set and whether it is of
        the type `FacadeVisitor`. If so, it invokes the `generic_visit` method of
        the root visitor, passing the specified node for processing. This allows
        for a centralized approach to handling PDF node traversal through the
        root visitor.

        :param node:    The PDF node to be visited, represented as a `PDFType`.
        :return:        True if the node was processed by the root visitor, False otherwise.
        """
        r: typing.Optional[NodeVisitor] = self.__root
        from borb.pdf.visitor.read.root_visitor import RootVisitor

        if r is not None and isinstance(r, RootVisitor):
            return r.visit(node=node)
        return None
