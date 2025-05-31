#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for converting PDF byte streams into a Document object.

The `DocumentVisitor` class implements the visitor pattern to traverse and process
the nodes of a PDF structure represented as a tree. This class is specifically designed
to handle the conversion of PDF bytes into a structured `Document` object, which can
facilitate further manipulation, rendering, or analysis of the PDF content.

By utilizing the visitor pattern, this class separates the algorithm for processing
PDF data from the structure of the PDF itself, promoting cleaner code and enhanced
maintainability. The `DocumentVisitor` class defines methods to visit various types
of nodes (such as pages, objects, or metadata) in the PDF tree, extracting relevant
information and assembling it into the `Document` object.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.pdf_bytes import PDFBytes
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class DocumentVisitor(ReadVisitor):
    """
    Visitor class for converting PDF byte streams into a Document object.

    The `DocumentVisitor` class implements the visitor pattern to traverse and process
    the nodes of a PDF structure represented as a tree. This class is specifically designed
    to handle the conversion of PDF bytes into a structured `Document` object, which can
    facilitate further manipulation, rendering, or analysis of the PDF content.

    By utilizing the visitor pattern, this class separates the algorithm for processing
    PDF data from the structure of the PDF itself, promoting cleaner code and enhanced
    maintainability. The `DocumentVisitor` class defines methods to visit various types
    of nodes (such as pages, objects, or metadata) in the PDF tree, extracting relevant
    information and assembling it into the `Document` object.
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
        self, node: typing.Union[int, bytes]
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
        if node != 0:
            return None

        # read first bytes
        # fmt: off
        pdf_start_byte_pos: int = PDFBytes.next_start_of_pdf_keyword(pdf_bytes=self.get_bytes(), start=0)

        # IF we can not find '%PDF-' in the file
        # THEN return None
        if pdf_start_byte_pos == -1:
            return None

        # IF the first bytes of the file do not start with '%PDF-'
        # THEN (left) trim the source until it starts as such
        if pdf_start_byte_pos != 0:
            self._ReadVisitor__root._RootVisitor__source = self._ReadVisitor__root._RootVisitor__source[pdf_start_byte_pos:]    # type: ignore[attr-defined]
        # fmt: on

        # go to end of file to find 'EOF'
        # fmt: off
        index_of_eof: int = PDFBytes.previous_eof_keyword(pdf_bytes=self.get_bytes(), start=len(self.get_bytes()))
        if index_of_eof == -1:
            return None
        # fmt: on

        # read number above %%EOF
        # fmt: off
        i: int = index_of_eof
        if self.get_bytes()[i-2:i] == b'\n\r':
            i -= 2
        if self.get_bytes()[i-2:i] == b'\r\n':
            i -= 2
        if self.get_bytes()[i-1:i] == b'\n':
            i -= 1
        if self.get_bytes()[i-1:i] == b'\r':
            i -= 1
        j: int = i - 1
        while self.get_bytes()[j:j+1] in b'0123456789':
            j -= 1
        j += 1
        start_of_xref: int = int(self.get_bytes()[j:i].decode().strip())
        # fmt: on

        # process (first) xref
        xref_and_j = self.root_generic_visit(start_of_xref)
        assert xref_and_j is not None
        xref, j = xref_and_j

        # IF the first bytes after start_of_xref are not 'xref'
        # THEN we have processed a stream (compressed) xref
        # AND we can expect the trailer dictionary somewhere else
        if self.get_bytes()[start_of_xref : start_of_xref + 4] != b"xref":
            start_of_trailer_dict_pos = PDFBytes.next_start_of_dictionary(
                pdf_bytes=self.get_bytes(), start=start_of_xref
            )

            # avoid using root_generic_visit
            # as this would only trigger another compressed_xref_visitor
            from borb.pdf.visitor.read.dict_visitor import DictVisitor

            dict_visitor: DictVisitor = next(
                iter(
                    [
                        x
                        for x in self._ReadVisitor__root._RootVisitor__visitors  # type: ignore[attr-defined]
                        if isinstance(x, DictVisitor)
                    ]
                )
            )
            trailer_dictionary_and_j = dict_visitor.visit(start_of_trailer_dict_pos)
        else:
            start_of_trailer_dict_pos = PDFBytes.next_start_of_dictionary(
                pdf_bytes=self.get_bytes(), start=j
            )
            trailer_dictionary_and_j = self.root_generic_visit(
                start_of_trailer_dict_pos
            )

        # process trailer dictionary
        # fmt: off
        assert trailer_dictionary_and_j is not None
        trailer_dictionary, j = trailer_dictionary_and_j
        assert isinstance(trailer_dictionary, dict)
        # fmt: on

        # populate a (proper) Document
        from borb.pdf.document import Document

        retval: Document = Document()
        retval["XRef"] = self._ReadVisitor__root._RootVisitor__xref  # type: ignore[attr-defined]
        retval["Trailer"] = trailer_dictionary

        # handle recursive references
        from borb.pdf.visitor.read.recursive_reference_visitor import (
            RecursiveReferenceVisitor,
        )

        retval = RecursiveReferenceVisitor().visit(retval)  # type: ignore[assignment]
        assert isinstance(retval, Document)

        # (back)link Page(s) to Document
        for i in range(0, retval.get_number_of_pages()):
            try:
                retval.get_page(i)._Page__document = retval  # type: ignore[attr-defined]
            except:
                pass

        # return
        return retval, len(self.get_bytes())
