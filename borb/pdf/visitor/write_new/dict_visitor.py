#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or persistence of dictionary objects within the PDF structure.

This class is responsible for traversing and processing nodes containing dictionaries
in the PDF document tree. It ensures that key-value pairs in the dictionaries are correctly
written or exported, handling the necessary formatting and encoding required for PDF
dictionaries.
"""

from borb.pdf.primitives import PDFType, stream
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class DictVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or persistence of dictionary objects within the PDF structure.

    This class is responsible for traversing and processing nodes containing dictionaries
    in the PDF document tree. It ensures that key-value pairs in the dictionaries are correctly
    written or exported, handling the necessary formatting and encoding required for PDF
    dictionaries.
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
        # check whether we have a dict
        if not isinstance(node, dict):
            return False
        if isinstance(node, stream):
            return False

        # start dictionary
        self._append_bytes(b"<<", trailing_space=False)

        # write_new pairs
        for k in sorted(node.keys()):

            # write_new key
            assert isinstance(k, str)
            self._append_bytes(f"/{k}".encode("latin1"))

            # write_new value
            v: PDFType = self.go_to_root_and_get_reference(node[k])
            self.go_to_root_and_visit(v)

        # end dictionary
        self._append_bytes(b">>", leading_space=False, trailing_space=False)

        # return
        return True
