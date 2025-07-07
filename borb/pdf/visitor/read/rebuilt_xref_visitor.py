#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RebuiltXREFVisitor is a low-level PDF visitor that scans the raw PDF byte stream
to reconstruct the cross-reference (XREF) table. It does so by identifying object
declarations of the form `<object_number> <generation_number> obj`, recording the
byte offset at which they occur, and registering these in the document's XREF table.

This is useful in damaged or linearized PDFs where the standard XREF table may be
incomplete or missing.
"""
import re
import typing

from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class RebuiltXREFVisitor(ReadVisitor):
    """
    A visitor that reconstructs the cross-reference (XREF) table by scanning the raw
    byte stream for object declarations. Matches lines like "12 0 obj" and records
    their position, building `reference` entries accordingly.

    This class can be used to recover XREF information when it is missing, corrupt,
    or incomplete.
    """

    OBJ_PATTERN: re.Pattern = re.compile(
        "(?P<on>[0123456789]+) (?P<gn>[0123456789]+) obj"
    )

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
        xref: typing.List[PDFType] = []
        i: int = 0
        while i < len(self.get_bytes()):
            # IF we did not read a number
            # THEN continue
            if self.get_bytes()[i] not in b"0123456789":
                i += 1
                continue

            try:
                window: str = self.get_bytes()[i : i + 32].decode("latin1")
                match: typing.Optional[re.Match] = RebuiltXREFVisitor.OBJ_PATTERN.match(
                    window
                )
                if match is not None:

                    # extract the numbers
                    object_number: int = int(match["on"])
                    generation_number: int = int(match["gn"])

                    # add to XREF
                    xref += [
                        reference(
                            object_nr=object_number,
                            generation_nr=generation_number,
                            byte_offset=i,
                            is_in_use=True,
                        )
                    ]
            except:
                pass

            # default
            i += 1

        # add to (root) xref tables
        self._ReadVisitor__root._RootVisitor__xref += xref  # type: ignore[attr-defined]

        # return
        return xref, -1
