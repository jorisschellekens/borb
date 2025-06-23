#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A facade class bundling multiple `WriteNewVisitor` objects.

The `FacadeVisitor` delegates the writing and persistence tasks of different sections
of a PDF document to specialized `WriteNewVisitor` instances. By grouping these
visitors, the `FacadeVisitor` simplifies the traversal and processing of various
document elements such as pages, text, and annotations. This ensures that each
section is handled properly, streamlining the PDF writing process.

This class serves as a central access point, facilitating easier extension or
modification of document writing behavior by coordinating multiple visitors.
"""
import typing

from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class FacadeVisitor(WriteNewVisitor):
    """
    A facade class bundling multiple `WriteNewVisitor` objects.

    The `FacadeVisitor` delegates the writing and persistence tasks of different sections
    of a PDF document to specialized `WriteNewVisitor` instances. By grouping these
    visitors, the `FacadeVisitor` simplifies the traversal and processing of various
    document elements such as pages, text, and annotations. This ensures that each
    section is handled properly, streamlining the PDF writing process.

    This class serves as a central access point, facilitating easier extension or
    modification of document writing behavior by coordinating multiple visitors.
    """

    __SPACE = b" "[0]
    __NEWLINE = b"\n"[0]

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the FacadeVisitor object to manage and coordinate multiple WriteNewVisitor instances.

        The constructor sets up the `FacadeVisitor` by preparing it to manage different
        `WriteNewVisitor` objects, each responsible for handling specific tasks like
        writing PDF pages, text, annotations, or other document elements. This
        initialization process enables the `FacadeVisitor` to serve as the central
        controller for document writing and persistence, ensuring that all sections
        of the PDF are handled by the appropriate visitor.
        """
        super().__init__()
        from borb.pdf.document import Document

        self.__document: typing.Optional[Document] = None
        # imports
        # fmt: off
        from borb.pdf.visitor.validate.validation_visitor import ValidationVisitor
        from borb.pdf.visitor.write_new.bool_visitor import BoolVisitor
        from borb.pdf.visitor.write_new.build_xref_visitor import BuildXRefVisitor
        from borb.pdf.visitor.write_new.default_stream_compression_visitor import DefaultStreamCompressionVisitor
        from borb.pdf.visitor.write_new.dict_visitor import DictVisitor
        from borb.pdf.visitor.write_new.document_visitor import DocumentVisitor
        from borb.pdf.visitor.write_new.float_visitor import FloatVisitor
        from borb.pdf.visitor.write_new.hex_str_visitor import HexStrVisitor
        from borb.pdf.visitor.write_new.inject_markinfo_visitor import InjectMarkInfoVisitor
        from borb.pdf.visitor.write_new.inject_srgb_outputintent_visitor import InjectsRGBOutputIntentVisitor
        from borb.pdf.visitor.write_new.inject_struct_tree_root_visitor import InjectStructTreeRootVisitor
        from borb.pdf.visitor.write_new.inject_version_as_comment_visitor import InjectVersionAsCommentVisitor
        from borb.pdf.visitor.write_new.inject_xmp_metadata_visitor import InjectXMPMetadataVisitor
        from borb.pdf.visitor.write_new.int_visitor import IntVisitor
        from borb.pdf.visitor.write_new.list_visitor import ListVisitor
        from borb.pdf.visitor.write_new.referenced_object_visitor import ReferencedObjectVisitor
        from borb.pdf.visitor.write_new.reference_visitor import ReferenceVisitor
        from borb.pdf.visitor.write_new.replace_str_by_name_visitor import ReplaceStrByNameVisitor
        from borb.pdf.visitor.write_new.stream_visitor import StreamVisitor
        from borb.pdf.visitor.write_new.str_visitor import StrVisitor
        from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor
        # fmt: on

        # build typing.List[WriteNewVisitor]
        self.__visitors: typing.List[WriteNewVisitor] = [  # type: ignore[annotation-unchecked]
            # PDF/A
            InjectMarkInfoVisitor(root=self),
            InjectsRGBOutputIntentVisitor(root=self),
            InjectStructTreeRootVisitor(root=self),
            InjectXMPMetadataVisitor(root=self),
            # XREF
            BuildXRefVisitor(root=self),
            # Usability
            ReplaceStrByNameVisitor(root=self),
            DefaultStreamCompressionVisitor(root=self),
            # Conformance
            ValidationVisitor(root=self),
            # Types (prio)
            DocumentVisitor(root=self),
            InjectVersionAsCommentVisitor(root=self),
            ReferencedObjectVisitor(root=self),
            # Types
            BoolVisitor(root=self),
            DictVisitor(root=self),
            FloatVisitor(root=self),
            HexStrVisitor(root=self),
            IntVisitor(root=self),
            ListVisitor(root=self),
            ReferenceVisitor(root=self),
            StreamVisitor(root=self),
            StrVisitor(root=self),
        ]

        self.__destination: bytes = b""  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    def _append_bytes(self, b: bytes) -> "FacadeVisitor":
        self.__destination += b
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
        return self.__destination

    def get_reference(self, node: PDFType) -> PDFType:
        """
        Retrieve the indirect reference corresponding to a given PDF node.

        This method attempts to locate an indirect reference within the document's
        cross-reference (XRef) table that points to the provided node. If a match is
        found, the corresponding `reference` object is returned. If no match is found,
        or if the document context is unavailable, the original node is returned.

        :param node:    The PDF node for which to retrieve the corresponding indirect reference.
        :return:        A `reference` object pointing to the node if found, otherwise the original node.
        """
        if self.__document is None:
            return node
        xref = self.__document.get("XRef", [])
        matching_reference: typing.Optional[reference] = next(
            iter([x for x in xref if id(x.get_referenced_object()) == id(node)]), None
        )
        if matching_reference is None:
            return node
        return matching_reference

    def tell(self) -> int:
        """
        Return the current position in the PDF content stream.

        This method returns the current size of the byte stream representing the
        PDF content being written. It is analogous to a "tell" method in a file
        object, where the value represents the position (in bytes) within the
        document output stream.

        :return: The current position in the PDF byte stream as an integer.
        """
        return len(self.__destination)

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
        from borb.pdf.document import Document

        if isinstance(node, Document):
            self.__document = node
        for v in self.__visitors:
            if v is self:
                continue
            if v.visit(node):
                return True
        # default case
        return False
