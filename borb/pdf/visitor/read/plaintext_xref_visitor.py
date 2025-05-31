#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing uncompressed cross-reference tables (XRef) in a PDF.

`PlaintextXRefVisitor` is specialized to locate and interpret plaintext (uncompressed)
cross-reference tables, which are integral to defining the byte offsets of objects
within the PDF file. Using the visitor pattern, `PlaintextXRefVisitor` parses each
entry in the XRef table, extracting information about object positions to enable
efficient access and retrieval during PDF parsing.

This class:
- Identifies the `xref` keyword marking the start of an uncompressed XRef table
- Processes entries with object offsets, generation numbers, and usage flags
- Builds an index mapping object numbers to their byte positions in the file,
  facilitating object lookup and retrieval

`PlaintextXRefVisitor` is essential for accurately mapping the structure of
PDFs that use uncompressed XRef tables, supporting document reconstruction and
efficient navigation within the PDF byte stream.
"""
import typing

from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.read.pdf_bytes import PDFBytes
from borb.pdf.visitor.read.xref_visitor import XRefVisitor


class PlaintextXRefVisitor(XRefVisitor):
    """
    Visitor class for reading and parsing uncompressed cross-reference tables (XRef) in a PDF.

    `PlaintextXRefVisitor` is specialized to locate and interpret plaintext (uncompressed)
    cross-reference tables, which are integral to defining the byte offsets of objects
    within the PDF file. Using the visitor pattern, `PlaintextXRefVisitor` parses each
    entry in the XRef table, extracting information about object positions to enable
    efficient access and retrieval during PDF parsing.

    This class:
    - Identifies the `xref` keyword marking the start of an uncompressed XRef table
    - Processes entries with object offsets, generation numbers, and usage flags
    - Builds an index mapping object numbers to their byte positions in the file,
      facilitating object lookup and retrieval

    `PlaintextXRefVisitor` is essential for accurately mapping the structure of
    PDFs that use uncompressed XRef tables, supporting document reconstruction and
    efficient navigation within the PDF byte stream.
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
    def visit(
        self, node: typing.Union[int, PDFType]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
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
        if not isinstance(node, int):
            return None

        # XREF should start with 'xref'
        if self.get_bytes()[node : node + 4] != b"xref":
            return None

        # read the start object nr
        i: int = PDFBytes.next_integer(pdf_bytes=self.get_bytes(), start=node)
        j: int = PDFBytes.next_space(pdf_bytes=self.get_bytes(), start=i + 1)
        start_object_nr: int = int(self.get_bytes()[i:j].decode())

        # read how many objects the XREF contains
        i = PDFBytes.next_integer(pdf_bytes=self.get_bytes(), start=j + 1)
        j = PDFBytes.next_newline(pdf_bytes=self.get_bytes(), start=i + 1)
        number_of_objects: int = int(self.get_bytes()[i:j].decode())

        # process each line of the XREF
        xref: typing.List[PDFType] = []
        for object_nr in range(start_object_nr, start_object_nr + number_of_objects):

            # read first number of each XREF line
            i = PDFBytes.next_integer(pdf_bytes=self.get_bytes(), start=j)
            j = PDFBytes.next_space(pdf_bytes=self.get_bytes(), start=i + 1)
            byte_offset: int = int(self.get_bytes()[i:j].decode())

            # read second nr
            i = PDFBytes.next_integer(pdf_bytes=self.get_bytes(), start=j + 1)
            j = PDFBytes.next_space(pdf_bytes=self.get_bytes(), start=i + 1)
            generation_number: int = int(self.get_bytes()[i:j].decode())

            # read 'f' or 'n'
            i = j + 1
            j = PDFBytes.next_newline(pdf_bytes=self.get_bytes(), start=i + 1)
            f_or_n: str = self.get_bytes()[i:j].decode()

            # add to XREF
            xref += [
                reference(
                    object_nr=object_nr,
                    generation_nr=generation_number,
                    byte_offset=byte_offset,
                    is_in_use=(f_or_n == "n"),
                )
            ]

        # add to (root) xref tables
        self._ReadVisitor__root._RootVisitor__xref += xref  # type: ignore[attr-defined]

        # IF the /Prev key has been set
        # THEN process the previous xref as well
        # fmt: off
        start_of_trailer_dict_pos = PDFBytes.next_start_of_dictionary(pdf_bytes=self.get_bytes(), start=j)
        end_of_trailer_dict_pos = self._get_matching_dictionary_close(start_of_dictionary_pos=start_of_trailer_dict_pos)
        prev = self._get_value_from_dictionary_bytes(from_byte=start_of_trailer_dict_pos,
                                                                            to_byte=end_of_trailer_dict_pos,
                                                                            key=b'Prev',
                                                                            default_value=None)
        if prev is not None:
            assert isinstance(prev, int)
            self.root_generic_visit(prev)

        # fmt: on

        # return
        return xref, j
