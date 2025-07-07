#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or persistence of stream objects within the PDF structure.

Stream objects in PDF documents typically represent binary data, such as images, fonts,
or embedded files. This class is responsible for traversing nodes that contain stream
data and writing them in the appropriate binary format. It ensures that the data is
correctly encoded, compressed (if necessary), and stored in compliance with PDF standards.
"""
import typing

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
        if not isinstance(node, stream):
            return False

        # start dictionary
        self._append_bytes_or_str("<<")

        # deflate the bytes
        deflated_bytes: bytes = node["Bytes"]

        # update /Length
        node["Length"] = len(deflated_bytes)

        # write_new pairs
        is_first_key: bool = True
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
            if is_first_key:
                self._append_bytes_or_str(f"/{k}")
                self._append_space_to_output_stream()
                is_first_key = False
            else:
                self._append_space_to_output_stream()
                self._append_bytes_or_str(f"/{k}")
                self._append_space_to_output_stream()

            # write_new value
            v: PDFType = self.go_to_root_and_get_reference(node[k])
            self.go_to_root_and_visit(v)

        # end dictionary
        self._append_bytes_or_str(">>\n")

        # begin stream
        self._append_bytes_or_str("stream\n")

        # stream bytes
        self._append_bytes_or_str(deflated_bytes)

        # end stream
        self._append_bytes_or_str(b"\nendstream")

        # return
        return True
