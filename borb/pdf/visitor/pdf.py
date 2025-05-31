#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a PDF document, providing methods for reading and writing PDF files.

The `PDF` class simplifies PDF handling by offering an interface for reading,
writing, and managing content within PDF documents. It abstracts the complexities
of PDF structure, allowing users to easily manipulate documents.
"""

import pathlib
import typing

from borb.pdf.document import Document


class PDF:
    """
    Represents a PDF document, providing methods for reading and writing PDF files.

    The `PDF` class simplifies PDF handling by offering an interface for reading,
    writing, and managing content within PDF documents. It abstracts the complexities
    of PDF structure, allowing users to easily manipulate documents.
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

    @staticmethod
    def read(where_from: typing.Union[str, pathlib.Path]) -> typing.Optional[Document]:
        """
        Read a PDF file from the specified location and convert it to a `Document` object.

        This method opens and reads a PDF file from disk, parses its contents, and
        converts the text and structure into a `Document` object. The input file
        location can be provided as a string or `pathlib.Path` object. The resulting
        `Document` object allows further manipulation and analysis of the PDF’s content
        within the application.

        :param where_from: The file path to the PDF, specified as a string or `pathlib.Path` object, indicating the location of the PDF file to read.
        :return: A `Document` object containing the parsed contents of the PDF, structured for further processing or display.
        """
        if isinstance(where_from, str):
            where_from = pathlib.Path(where_from)
        assert isinstance(where_from, pathlib.Path)
        assert where_from.exists()

        # read all bytes
        bts: bytes = b""
        with open(where_from, "rb") as pdf_file_handle:
            bts = pdf_file_handle.read()

        # instantiate FacadeVisitor
        from borb.pdf.visitor.read.root_visitor import RootVisitor

        rv = RootVisitor()
        document_and_index = rv.visit(bts)
        if document_and_index is None:
            return None
        assert isinstance(document_and_index[0], Document)

        # return
        return document_and_index[0]

    @staticmethod
    def write(
        what: Document,
        where_to: typing.Union[str, pathlib.Path],
    ) -> None:
        """
        Write the specified Document to a PDF file.

        This method saves the provided Document object into a PDF format at the
        location specified by the file path. The file path can be a string or
        a pathlib.Path object. If the file already exists, it will be overwritten.

        :param where_to:    the path (or pathlib.Path) where the Document needs to be stored
        :param what:        the document to be stored
        :return:    None
        """
        # convert to pathlib.Path
        if isinstance(where_to, str):
            where_to = pathlib.Path(where_to)
            if not where_to.parent.exists():
                where_to.parent.mkdir(parents=True)
        assert isinstance(where_to, pathlib.Path)

        # make sure the pathlib.Path exists
        assert where_to.parent.exists()

        # instantiate FacadeVisitor
        from borb.pdf.visitor.write_new.facade_visitor import FacadeVisitor

        rv: FacadeVisitor = FacadeVisitor()

        # convert everything to bytes using visitor design pattern
        rv.visit(node=what)

        # persist
        with open(where_to, "wb") as pdf_file_handle:
            pdf_file_handle.write(rv.bytes())
