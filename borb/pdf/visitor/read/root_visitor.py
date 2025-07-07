#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for traversing and processing a PDF document tree.

`FacadeVisitor` implements the visitor pattern to traverse a PDF document
and process different types of nodes within the document. It coordinates
the execution of specialized visitor classes that handle various aspects
of the PDF, such as objects, references, dictionaries, and primitive types.
This class serves as the root visitor for handling and dispatching nodes
to the appropriate handler, allowing for efficient and extensible parsing
and processing of a PDF document.

Key responsibilities:
- Initializes a list of specialized visitors for processing various parts
  of the PDF document (e.g., objects, dictionaries, strings, etc.).
- Provides a `generic_visit` method that serves as the default entry point
  for traversing the document. This method dispatches nodes to the correct
  visitor for handling based on the type of node.
- Handles the overall traversal of the PDF document using a set of visitor
  classes, which process each part of the document as defined by the PDF
  specification.
"""
import typing

from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class RootVisitor(ReadVisitor):
    """
    Visitor class for traversing and processing a PDF document tree.

    `FacadeVisitor` implements the visitor pattern to traverse a PDF document
    and process different types of nodes within the document. It coordinates
    the execution of specialized visitor classes that handle various aspects
    of the PDF, such as objects, references, dictionaries, and primitive types.
    This class serves as the root visitor for handling and dispatching nodes
    to the appropriate handler, allowing for efficient and extensible parsing
    and processing of a PDF document.

    Key responsibilities:
    - Initializes a list of specialized visitors for processing various parts
      of the PDF document (e.g., objects, dictionaries, strings, etc.).
    - Provides a `generic_visit` method that serves as the default entry point
      for traversing the document. This method dispatches nodes to the correct
      visitor for handling based on the type of node.
    - Handles the overall traversal of the PDF document using a set of visitor
      classes, which process each part of the document as defined by the PDF
      specification.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the FacadeVisitor instance and set up the necessary visitors for processing a PDF document.

        This constructor initializes the `FacadeVisitor` by setting up an empty
        list of cross-reference tables (`__xref_tables`), loading required
        visitor classes, and creating a list of visitors to handle different
        parts of the PDF document. It also initializes an empty `__source`
        byte string, which will be populated during traversal.

        The visitor classes are responsible for handling different aspects of the
        PDF document, including processing objects, dictionaries, lists, strings,
        and primitive types. The `FacadeVisitor` acts as the central coordinator
        for dispatching PDF nodes to the appropriate visitor.
        """
        super().__init__(root=self)
        from borb.pdf.visitor.read.read_visitor import ReadVisitor
        from borb.pdf.visitor.read.document_visitor import DocumentVisitor
        from borb.pdf.visitor.read.plaintext_xref_visitor import PlaintextXRefVisitor
        from borb.pdf.visitor.read.dict_visitor import DictVisitor
        from borb.pdf.visitor.read.list_visitor import ListVisitor
        from borb.pdf.visitor.read.str_visitor import StrVisitor
        from borb.pdf.visitor.read.hex_str_visitor import HexStrVisitor
        from borb.pdf.visitor.read.reference_visitor import ReferenceVisitor
        from borb.pdf.visitor.read.obj_visitor import ObjVisitor
        from borb.pdf.visitor.read.name_visitor import NameVisitor
        from borb.pdf.visitor.read.float_visitor import FloatVisitor
        from borb.pdf.visitor.read.int_visitor import IntVisitor
        from borb.pdf.visitor.read.bool_visitor import BoolVisitor
        from borb.pdf.visitor.read.compressed_xref_visitor import CompressedXRefVisitor
        from borb.pdf.visitor.read.null_visitor import NullVisitor
        from borb.pdf.visitor.read.date_str_visitor import DateStrVisitor

        self.__visitors: typing.List[ReadVisitor] = [  # type: ignore[annotation-unchecked]
            DocumentVisitor(root=self),
            PlaintextXRefVisitor(root=self),
            CompressedXRefVisitor(root=self),
            ObjVisitor(root=self),
            # aggregation types
            DictVisitor(root=self),
            ListVisitor(root=self),
            # reference type
            ReferenceVisitor(root=self),
            # primitive types
            DateStrVisitor(root=self),
            StrVisitor(root=self),
            HexStrVisitor(root=self),
            NullVisitor(root=self),
            NameVisitor(root=self),
            BoolVisitor(root=self),
            FloatVisitor(root=self),
            IntVisitor(root=self),
        ]
        self.__source: bytes = b""  # type: ignore[annotation-unchecked]
        self.__references_being_resolved: typing.List[reference] = []  # type: ignore[annotation-unchecked]
        self.__xref: typing.List[reference] = []  # type: ignore[annotation-unchecked]
        self.__cache: typing.Dict[int, typing.Any] = {}

    #
    # PRIVATE
    #

    @staticmethod
    def __get_stack_size(size=2):
        """Get stack size for caller's frame."""
        import sys
        from itertools import count

        frame = sys._getframe(size)
        for size in count(size):
            frame = frame.f_back
            if not frame:
                return size
        return 0

    #
    # PUBLIC
    #

    def visit(
        self, node: typing.Union[bytes, PDFType]
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
        if (
            isinstance(self, RootVisitor)
            and isinstance(node, bytes)
            and self.__source == b""
        ):
            self.__source = node
            node = 0
        # print(f'stack depth: {RootVisitor.__get_stack_size()}, byte pos: {node}')
        if isinstance(node, int) and node in self.__cache:
            return self.__cache[node]
        for v in self.__visitors:
            if v is self:
                continue
            w = v.visit(node)
            if w is not None:
                # store in cache
                if (
                    isinstance(node, int)
                    and isinstance(w, tuple)
                    and len(w) == 2
                    and isinstance(w[1], int)
                    and abs(w[1] - node) > 256
                ):
                    self.__cache[node] = w
                # return
                return w
        # debug
        if isinstance(node, int):
            print(f"unable to map bytes[{node}:]")
        # default case
        return None
