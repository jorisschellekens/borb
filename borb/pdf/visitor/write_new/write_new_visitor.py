#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the base class for visitor objects that traverse and write or persist a PDF document structure.

This class inherits from `NodeVisitor` and serves as a foundation for specialized
visitor classes that handle writing operations for different parts of a PDF (e.g., pages,
text, images, annotations). It provides a framework for persisting the structure by
traversing the nodes of a PDF document tree.

The separation of writing operations from the PDF components allows for easy extension
or modification through subclasses tailored to specific node types.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.node_visitor import NodeVisitor


class WriteNewVisitor(NodeVisitor):
    """
    Represents the base class for visitor objects that traverse and write or persist a PDF document structure.

    This class inherits from `NodeVisitor` and serves as a foundation for specialized
    visitor classes that handle writing operations for different parts of a PDF (e.g., pages,
    text, images, annotations). It provides a framework for persisting the structure by
    traversing the nodes of a PDF document tree.

    The separation of writing operations from the PDF components allows for easy extension
    or modification through subclasses tailored to specific node types.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, root: typing.Optional[NodeVisitor] = None) -> None:
        """
        Initialize a `WriteNewVisitor` instance.

        This constructor sets up the base functionality for the `WriteNewVisitor` class,
        which is designed to traverse and write or persist the structure of a PDF document.

        :param root:    The root visitor node of the document's structure. It can be a `NodeVisitor`
                        object representing the starting point of the document traversal or `None`
                        if the root node is not provided. Defaults to `None`.
        """
        super().__init__()
        self.__root: typing.Optional[NodeVisitor] = root

    #
    # PRIVATE
    #

    def _append_bytes_or_str(
        self, bytes_or_str: typing.Union[bytes, str]
    ) -> "WriteNewVisitor":
        # IF the root is None
        # THEN return
        root: typing.Optional[NodeVisitor] = self.__root
        if root is None:
            return self

        # IF the root is not a FacadeVisitor
        # THEN return
        from borb.pdf.visitor.write_new.facade_visitor import FacadeVisitor

        if not isinstance(root, FacadeVisitor):
            return self

        # IF we are dealing with str
        # THEN convert to bytes
        bts = b""
        if isinstance(bytes_or_str, bytes):
            bts = bytes_or_str
        if isinstance(bytes_or_str, str):
            bts = bytes_or_str.encode("latin1")

        # append
        root._append_bytes(bts)

        # return
        return self

    def _append_newline_to_output_stream(self) -> "WriteNewVisitor":
        # IF the root is None
        # THEN return
        root: typing.Optional[NodeVisitor] = self.__root
        if root is None:
            return self

        # IF the root is not a FacadeVisitor
        # THEN return
        from borb.pdf.visitor.write_new.facade_visitor import FacadeVisitor

        if not isinstance(root, FacadeVisitor):
            return self

        # IF we have not yet persisted any bytes
        # THEN the space is not needed
        if len(root.bytes()) == 0:
            return self

        # IF the last character persisted was a newline
        # THEN newline is not needed
        if root.bytes()[-1] == b"\n"[0]:
            return self

        root._append_bytes(b"\n")
        return self

    def _append_space_to_output_stream(self) -> "WriteNewVisitor":
        # IF the root is None
        # THEN return
        root: typing.Optional[NodeVisitor] = self.__root
        if root is None:
            return self

        # IF the root is not a FacadeVisitor
        # THEN return
        from borb.pdf.visitor.write_new.facade_visitor import FacadeVisitor

        if not isinstance(root, FacadeVisitor):
            return self

        # IF we have not yet persisted any bytes
        # THEN the space is not needed
        if len(root.bytes()) == 0:
            return self

        # IF the last character persisted was a newline
        # THEN newline is not needed
        if root.bytes()[-1] == b" "[0]:
            return self

        root._append_bytes(b" ")
        return self

    #
    # PUBLIC
    #

    def bytes(self) -> bytes:
        """
        Return the byte representation of the written PDF content.

        This method retrieves the accumulated bytes from the PDF writing process,
        which represents the final content of the PDF document. The byte data
        includes all elements processed by the visitor and is suitable for saving
        or further processing, such as writing to a file or sending over a network.

        :return: A `bytes` object containing the written PDF content.
        """
        r: typing.Optional[NodeVisitor] = self.__root
        from borb.pdf.visitor.write_new.facade_visitor import FacadeVisitor

        if r is not None and isinstance(r, FacadeVisitor):
            return r.bytes()
        return b""

    def go_to_root_and_get_reference(self, node: typing.Any) -> PDFType:
        """
        Resolve the indirect reference of a PDF node via the root visitor.

        This method delegates the task of resolving a PDF node to its underlying
        object (e.g., resolving indirect references) to the root visitor, assuming
        one is available. If the root visitor is present and provides a valid reference
        for the given node, that reference is returned. Otherwise, the original node is
        returned unmodified.

        :param node:    The PDF node to resolve, typically an indirect reference or container.
        :return:        The resolved node if successful, or the original node if resolution fails or no root visitor is set.
        """
        if self.__root is None:
            return node
        try:
            return self.__root.get_reference(node)  # type: ignore[attr-defined]
        except:
            pass
        return node

    def go_to_root_and_visit(self, node: typing.Any) -> typing.Optional[typing.Any]:
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
        if self.__root is None:
            return False
        return self.__root.visit(node=node)

    def tell(self) -> int:
        """
        Return the current position in the PDF content stream.

        This method returns the current size of the byte stream representing the
        PDF content being written. It is analogous to a "tell" method in a file
        object, where the value represents the position (in bytes) within the
        document output stream.

        :return: The current position in the PDF byte stream as an integer.
        """
        r: typing.Optional[NodeVisitor] = self.__root
        from borb.pdf.visitor.write_new.facade_visitor import FacadeVisitor

        if r is not None and isinstance(r, FacadeVisitor):
            return r.tell()
        return -1
