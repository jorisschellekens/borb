#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor that writes referenced PDF objects in 'obj ... endobj' form.

This class is part of the PDF serialization pipeline in borb. It handles
objects that are indirectly referenced (i.e., those with an object number
and generation number) and emits their serialized representation in
accordance with the PDF specification.

It expects each visited node to be an instance of `ReferencedObjectType`,
which bundles a `reference` with its associated `PDFType` object.

The output follows this structure:
    <object_nr> <generation_nr> obj
    <serialized object>
    endobj
"""
import typing

from borb.pdf.primitives import reference, PDFType
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class ReferencedObjectVisitor(WriteNewVisitor):
    """
    Visitor that writes referenced PDF objects in 'obj ... endobj' form.

    This class is part of the PDF serialization pipeline in borb. It handles
    objects that are indirectly referenced (i.e., those with an object number
    and generation number) and emits their serialized representation in
    accordance with the PDF specification.

    It expects each visited node to be an instance of `ReferencedObjectType`,
    which bundles a `reference` with its associated `PDFType` object.

    The output follows this structure:
        <object_nr> <generation_nr> obj
        <serialized object>
        endobj
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
        from borb.pdf.visitor.write_new.document_visitor import ReferencedObjectType

        if not isinstance(node, ReferencedObjectType):
            return False

        # unpack tuple
        ref: reference = node.reference  # type: ignore[attr-defined]
        obj: PDFType = node.object  # type: ignore[attr-defined]

        # recurse
        self._append_bytes_or_str(
            f"{ref.get_object_nr()} {ref.get_generation_nr()} obj\n"
        )

        # recurse
        self.go_to_root_and_visit(obj)

        # newline
        self._append_newline_to_output_stream()

        # end object
        self._append_bytes_or_str("endobj\n\n")

        # return
        return True
