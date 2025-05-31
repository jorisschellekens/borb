#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or persistence of stream objects within the PDF structure.

Stream objects in PDF documents typically represent binary data, such as images, fonts,
or embedded files. This class is responsible for traversing nodes that contain stream
data and writing them in the appropriate binary format. It ensures that the data is
correctly encoded, compressed (if necessary), and stored in compliance with PDF standards.
"""

from borb.pdf.primitives import PDFType, stream
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class StreamVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or persistence of stream objects within the PDF structure.

    Stream objects in PDF documents typically represent binary data, such as images, fonts,
    or embedded files. This class is responsible for traversing nodes that contain stream
    data and writing them in the appropriate binary format. It ensures that the data is
    correctly encoded, compressed (if necessary), and stored in compliance with PDF standards.
    """

    __FORCE_COMPRESSION_WHEN_FILTER_IS_NOT_SET: bool = True

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def visit(self, node: PDFType) -> bool:
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
        if not isinstance(node, stream):
            return False

        # start dictionary
        self._append_bytes(b"<<", trailing_space=False)

        # deflate the bytes
        deflated_bytes: bytes = node["Bytes"]

        # update /Length
        node["Length"] = len(deflated_bytes)

        # write_new pairs
        for k in sorted(node.keys()):

            # skip /Bytes
            if k == "Bytes":
                continue
            if k == "DecodedBytes":
                continue

            # Skip /Filter None
            if k == "Filter" and node[k] is None:
                continue

            # write_new key
            assert isinstance(k, str)
            self._append_bytes(f"/{k}".encode("latin1"))

            # write_new value
            v: PDFType = self.go_to_root_and_get_reference(node[k])
            self.go_to_root_and_visit(v)

        # end dictionary
        self._append_bytes(b">>\n", leading_space=False, trailing_space=False)

        # begin stream
        self._append_bytes(b"stream\n", leading_space=False, trailing_space=False)

        # stream bytes
        self._append_bytes(deflated_bytes, leading_space=False, trailing_space=False)

        # end stream
        self._append_bytes(b"\nendstream", leading_space=False, trailing_space=False)

        # return
        return True
