#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class for handling the writing or persistence of document-level structures within the PDF.

This class is responsible for traversing and processing the top-level components of a PDF
document, such as metadata, pages, and overall structure. It ensures that all essential
elements of the document are correctly written and formatted in accordance with PDF standards.
"""


import typing

from borb.pdf.document import Document
from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class DocumentVisitor(WriteNewVisitor):
    """
    A visitor class for handling the writing or persistence of document-level structures within the PDF.

    This class is responsible for traversing and processing the top-level components of a PDF
    document, such as metadata, pages, and overall structure. It ensures that all essential
    elements of the document are correctly written and formatted in accordance with PDF standards.
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
        # check whether this is a document
        if not isinstance(node, Document):
            return False
        if "XRef" not in node:
            return False
        if len(node["XRef"]) == 0:
            return False
        if "Trailer" not in node:
            return False

        # write_new header
        self._append_bytes(b"%PDF-1.7\n", leading_space=False, trailing_space=False)

        # write 4 bytes
        # fmt: off
        self._append_bytes(b"%", leading_space=False, trailing_space=False)
        self._append_bytes(bytes([226, 227, 207, 211]), leading_space=False, trailing_space=False)
        self._append_bytes(b"\n", leading_space=False, trailing_space=False)
        # fmt: on

        # write_new objects
        xref: typing.List[reference] = node["XRef"]
        for i, xref_entry in enumerate(xref):

            # IF we are handling the special '0 65535 R'
            # THEN skip
            if (
                xref_entry.get_object_nr() == 0
                and xref_entry.get_generation_nr() == 65535
            ):
                continue

            # IF the xref entry is not in use
            # THEN don't write it
            if not xref_entry.is_in_use():
                continue

            # IF the xref entry does not have an associated object
            # THEN don't write it AND mark the object as 'not in use'
            if xref_entry.get_referenced_object() is None:
                xref[i] = reference(
                    object_nr=xref_entry.get_object_nr(),
                    generation_nr=xref_entry.get_generation_nr(),
                    byte_offset=65535,
                    referenced_object=None,
                    id=xref_entry.get_id(),
                    is_in_use=False,
                )
                continue

            # start obj
            xref[i] = reference(
                object_nr=xref_entry.get_object_nr(),
                generation_nr=xref_entry.get_generation_nr(),
                byte_offset=self.tell(),
                referenced_object=xref_entry.get_referenced_object(),
                id=xref_entry.get_id(),
            )
            self._append_bytes(
                f"{xref_entry.get_object_nr()} {xref_entry.get_generation_nr()} obj\n".encode(
                    "latin1"
                ),
                leading_space=False,
                trailing_space=False,
            )

            # recursion
            referenced_object: typing.Optional[PDFType] = (
                xref_entry.get_referenced_object()
            )
            assert referenced_object is not None
            self.go_to_root_and_visit(referenced_object)

            # newline
            self._append_bytes(b"\n", leading_space=False, trailing_space=False)

            # end object
            self._append_bytes(b"endobj\n", leading_space=False, trailing_space=False)

        # write_new xref
        xref_tell: int = self.tell()
        self._append_bytes(b"xref\n")
        self._append_bytes(f"0 {len(xref)+1}\n".encode("latin1"))
        self._append_bytes("0000000000 65535 f\r\n".encode("latin1"))
        for xref_entry in xref:
            self._append_bytes(
                f"{xref_entry.get_byte_offset():010d} 00000 n\r\n".encode("latin1")
            )

        # write_new trailer
        self._append_bytes(b"trailer\n", leading_space=False, trailing_space=False)
        self.go_to_root_and_visit(node["Trailer"])
        self._append_bytes(b"\n")

        # write_new xref
        self._append_bytes(b"startxref\n", leading_space=False, trailing_space=False)

        # write_new
        self._append_bytes(
            f"{xref_tell}\n".encode("latin1"), leading_space=False, trailing_space=False
        )

        # write_new EOF
        self._append_bytes(b"%%EOF\n", leading_space=False, trailing_space=False)

        # return
        return True
