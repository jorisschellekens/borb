#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor that compresses the streams within a PDF document using the 'FlateDecode' filter and zlib compression algorithm.

This visitor is designed to compress streams that are decoded but have
no existing compressed byte data. It only works on streams that contain
the appropriate 'DecodedBytes' and 'Filter' attributes for the stream objects.
"""
import typing

from borb.pdf import Document
from borb.pdf.primitives import stream, name, reference
from borb.pdf.visitor.node_visitor import NodeVisitor
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class DefaultStreamCompressionVisitor(WriteNewVisitor):
    """
    A visitor that compresses the streams within a PDF document using the 'FlateDecode' filter and zlib compression algorithm.

    This visitor is designed to compress streams that are decoded but have
    no existing compressed byte data. It only works on streams that contain
    the appropriate 'DecodedBytes' and 'Filter' attributes for the stream objects.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, root: typing.Optional[NodeVisitor] = None) -> None:
        """
        Initialize the DefaultStreamCompressionVisitor.

        :param root: Optional root visitor to start the traversal of the document.
        """
        super().__init__(root=root)
        self.__has_been_used: bool = False

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
        if not isinstance(node, Document):
            return False
        if self.__has_been_used:
            return False

        import zlib

        for ref in node.get("XRef", []):
            if not isinstance(ref, reference):
                continue
            obj = ref.get_referenced_object()
            if not isinstance(obj, stream):
                continue
            if "DecodedBytes" not in obj:
                continue
            if (
                "Bytes" in obj
                and isinstance(obj.get("Bytes"), bytes)
                and len(obj.get("Bytes")) != 0  # type: ignore[arg-type]
            ):
                continue
            if "Filter" in obj and obj["Filter"] not in ["FL", "FlateDecode"]:
                continue

            # compression
            obj[name("Bytes")] = zlib.compress(obj["DecodedBytes"], level=9)
            obj[name("Filter")] = name("FlateDecode")
            obj[name("Length")] = len(obj["Bytes"])

        # call root
        self.__has_been_used = True
        super().go_to_root_and_visit(node=node)

        # return
        return True
