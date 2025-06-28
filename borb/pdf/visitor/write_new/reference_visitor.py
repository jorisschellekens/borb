#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or processing of reference objects within the PDF structure.

The `ReferenceVisitor` class is responsible for traversing and processing nodes
that contain references in the PDF document tree. It ensures that reference
objects are correctly written or exported, managing the necessary formatting,
resolution of reference links, and any specific requirements related to PDF references.

This class inherits from the `WriteNewVisitor` class, providing a consistent
approach to processing reference nodes while maintaining the integrity of the
document structure.
"""
import typing

from borb.pdf.primitives import reference
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class ReferenceVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or processing of reference objects within the PDF structure.

    The `ReferenceVisitor` class is responsible for traversing and processing nodes
    that contain references in the PDF document tree. It ensures that reference
    objects are correctly written or exported, managing the necessary formatting,
    resolution of reference links, and any specific requirements related to PDF references.

    This class inherits from the `WriteNewVisitor` class, providing a consistent
    approach to processing reference nodes while maintaining the integrity of the
    document structure.
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
        if not isinstance(node, reference):
            return False

        # default
        self._append_bytes_or_str(
            f"{node.get_object_nr()} {node.get_generation_nr()} R"
        )
        return True
