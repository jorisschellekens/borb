#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or persistence of list objects within the PDF structure.

This class is responsible for traversing and processing nodes that contain list data
in the PDF document tree. It ensures that each element of the list is correctly written
or exported, managing the necessary formatting and encoding to adhere to PDF standards.
"""
import typing

from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class ListVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or persistence of list objects within the PDF structure.

    This class is responsible for traversing and processing nodes that contain list data
    in the PDF document tree. It ensures that each element of the list is correctly written
    or exported, managing the necessary formatting and encoding to adhere to PDF standards.
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
        # check whether we have a list
        if not isinstance(node, list):
            return False

        # start list
        self._append_bytes_or_str("[")

        # recurse
        N: int = len(node)
        for i in range(0, N):
            self.go_to_root_and_visit(self.go_to_root_and_get_reference(node[i]))
            if i != N - 1:
                self._append_space_to_output_stream()

        # end list
        self._append_bytes_or_str("]")

        # default
        return True
