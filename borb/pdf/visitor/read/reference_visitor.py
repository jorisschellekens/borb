#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing indirect references in a PDF byte stream.

`ReferenceVisitor` is specialized to identify and process indirect references
in a PDF, which link to other objects within the document by their object
number and generation. Using the visitor pattern, `ReferenceVisitor` parses
these references, allowing for efficient cross-referencing between objects
during PDF parsing.

This class:
- Recognizes the format of indirect references (`<object_number> <generation> R`)
- Extracts the referenced object number and generation for lookup
- Supports recursive traversal, enabling accurate reconstruction of nested structures

`ReferenceVisitor` is essential for managing PDF document structure, as it allows
references to be resolved and processed within a comprehensive parsing framework.
"""
import typing

from borb.pdf.primitives import PDFType, reference, stream
from borb.pdf.visitor.read.compressed_xref_visitor import CompressedXRefVisitor
from borb.pdf.visitor.read.compression.decode_stream import decode_stream
from borb.pdf.visitor.read.document_visitor import DocumentVisitor
from borb.pdf.visitor.read.no_op_reference_visitor import NoOpReferenceVisitor
from borb.pdf.visitor.read.plaintext_xref_visitor import PlaintextXRefVisitor
from borb.pdf.visitor.read.read_visitor import ReadVisitor
from borb.pdf.visitor.read.root_visitor import RootVisitor


class ReferenceVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing indirect references in a PDF byte stream.

    `ReferenceVisitor` is specialized to identify and process indirect references
    in a PDF, which link to other objects within the document by their object
    number and generation. Using the visitor pattern, `ReferenceVisitor` parses
    these references, allowing for efficient cross-referencing between objects
    during PDF parsing.

    This class:
    - Recognizes the format of indirect references (`<object_number> <generation> R`)
    - Extracts the referenced object number and generation for lookup
    - Supports recursive traversal, enabling accurate reconstruction of nested structures

    `ReferenceVisitor` is essential for managing PDF document structure, as it allows
    references to be resolved and processed within a comprehensive parsing framework.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def __get_modified_root_visitor(self) -> ReadVisitor:
        # build a (modified) FacadeVisitor
        # fmt: off
        rv = RootVisitor()
        rv._RootVisitor__visitors = [x for x in rv._RootVisitor__visitors if not isinstance(x, DocumentVisitor)]                                        # type: ignore[attr-defined]
        rv._RootVisitor__visitors = [x for x in rv._RootVisitor__visitors if not isinstance(x, PlaintextXRefVisitor)]                                   # type: ignore[attr-defined]
        rv._RootVisitor__visitors = [x for x in rv._RootVisitor__visitors if not isinstance(x, CompressedXRefVisitor)]                                  # type: ignore[attr-defined]
        rv._RootVisitor__visitors = [x if not isinstance(x, ReferenceVisitor) else NoOpReferenceVisitor(root=rv) for x in rv._RootVisitor__visitors]    # type: ignore[attr-defined]
        rv._ReadVisitor__root._RootVisitor__xref = self._ReadVisitor__root._RootVisitor__xref                                                           # type: ignore[attr-defined]
        # fmt: on

        # return
        return rv

    def __look_up_reference(
        self, object_nr: int, generation_nr: int
    ) -> typing.Optional[reference]:
        for xref_table_entry in self._ReadVisitor__root._RootVisitor__xref[::-1]:  # type: ignore[attr-defined]
            if (
                xref_table_entry.get_object_nr() == object_nr
                and xref_table_entry.get_generation_nr() == generation_nr
            ):
                return xref_table_entry
        return None

    def __mark_reference_as_being_resolved(self, r: reference):
        self._ReadVisitor__root._RootVisitor__references_being_resolved += [r]  # type: ignore[attr-defined]

    def __reference_is_being_resolved(self, r: reference) -> bool:
        for ref in self._ReadVisitor__root._RootVisitor__references_being_resolved:  # type: ignore[attr-defined]
            if ref.get_object_nr() != r.get_object_nr():
                continue
            if ref.get_generation_nr() != r.get_generation_nr():
                continue
            if ref.get_byte_offset() != r.get_byte_offset():
                continue
            return True
        return False

    def __resolve_references(self, o: PDFType) -> PDFType:
        if isinstance(o, list):
            return [self.__resolve_references(x) for x in o]
        if isinstance(o, dict):
            return {k: self.__resolve_references(v) for k, v in o.items()}
        if isinstance(o, reference):
            object_nr: typing.Optional[int] = o.get_object_nr()
            generation_nr: typing.Optional[int] = o.get_generation_nr()
            assert object_nr is not None
            assert generation_nr is not None
            o = (
                self.__look_up_reference(
                    object_nr=object_nr, generation_nr=generation_nr
                )
                or o
            )
            return self.__visit_reference(o)
        return o

    def __visit_byte_offset_reference(self, r: reference) -> typing.Optional[PDFType]:

        # attempt to resolve the reference
        try:
            byte_offset: typing.Optional[int] = r.get_byte_offset()
            assert byte_offset is not None
            referenced_object_and_blank = self.root_generic_visit(byte_offset)
            if referenced_object_and_blank is None:
                print(
                    f"Unable to resolve {r.get_object_nr()} {r.get_generation_nr()} R (redirects to byte {r.get_byte_offset()}), read returns None"
                )
                return r
            return referenced_object_and_blank[0]
        except Exception as e:
            print(
                f"Unable to resolve {r.get_object_nr()} {r.get_generation_nr()} R (redirects to byte {r.get_byte_offset()}), read raises {e}"
            )
            return None

    def __visit_object_stm_reference(self, r: reference) -> typing.Optional[PDFType]:
        parent_stream_object_nr: typing.Optional[int] = r.get_parent_stream_object_nr()
        index_in_parent_stream: typing.Optional[int] = r.get_index_in_parent_stream()
        assert parent_stream_object_nr is not None
        assert index_in_parent_stream is not None
        r2: typing.Optional[reference] = self.__look_up_reference(
            object_nr=parent_stream_object_nr, generation_nr=0
        )

        try:
            assert r2 is not None
            byte_offset: typing.Optional[int] = r2.get_byte_offset()
            assert byte_offset is not None
            referenced_object_and_blank = self.root_generic_visit(byte_offset)
            if referenced_object_and_blank is None:
                return None
        except:
            return None

        # get the object stream
        object_stm = referenced_object_and_blank[0]
        assert isinstance(object_stm, stream)

        # decode
        decode_stream(object_stm)

        # decode the bytes
        # fmt: off
        header_offset: int = object_stm.get("First", 0)
        object_stm_header: bytes = object_stm["DecodedBytes"][:header_offset]
        object_stm_bytes_without_header: bytes = object_stm["DecodedBytes"][header_offset:]
        # fmt: on

        objs: typing.List[PDFType] = []
        while len(object_stm_bytes_without_header) > 0:

            # IF we see a space
            # THEN skip
            if object_stm_bytes_without_header[0:1] == b" ":
                object_stm_bytes_without_header = object_stm_bytes_without_header[1:]
                continue

            # IF we see a newline (\n\r)
            # THEN skip
            if object_stm_bytes_without_header[0:2] == b"\n\r":
                object_stm_bytes_without_header = object_stm_bytes_without_header[2:]
                continue
            if object_stm_bytes_without_header[0:2] == b"\r\n":
                object_stm_bytes_without_header = object_stm_bytes_without_header[2:]
                continue
            if object_stm_bytes_without_header[0:1] == b"\n":
                object_stm_bytes_without_header = object_stm_bytes_without_header[1:]
                continue
            if object_stm_bytes_without_header[0:1] == b"\r":
                object_stm_bytes_without_header = object_stm_bytes_without_header[1:]
                continue

            rv = self.__get_modified_root_visitor()
            rv._ReadVisitor__root._RootVisitor__source = b""  # type: ignore[attr-defined]
            referenced_object_and_i = rv.visit(object_stm_bytes_without_header)
            if referenced_object_and_i is None:
                break
            objs += [referenced_object_and_i[0]]
            object_stm_bytes_without_header = object_stm_bytes_without_header[
                referenced_object_and_i[1] :
            ]

        # header:  list of object numbers and their offsets (within the stream)
        header: typing.List[int] = [int(x) for x in object_stm_header.split()]

        # return
        referenced_object = objs[index_in_parent_stream]
        referenced_object = self.__resolve_references(referenced_object)
        return referenced_object

    def __visit_reference(self, r: reference) -> typing.Optional[PDFType]:
        # IF we are already resolving that reference (for instance /Parent)
        # THEN do not attempt to visit the byte offset
        if self.__reference_is_being_resolved(r):
            return r

        # mark reference as being resolved
        self.__mark_reference_as_being_resolved(r)

        # IF we have already resolved the reference in the past
        # THEN simply return that item
        if r.get_referenced_object() is not None:
            return r.get_referenced_object()

        # IF the reference has a parent stream
        # THEN call __visit_object_stm_reference
        if r.get_index_in_parent_stream() is not None:
            retval = self.__visit_object_stm_reference(r) or r, -1
            r._reference__referenced_object = retval[0]
            return r.get_referenced_object()

        # IF the reference has a byte offset
        # THEN call  __visit_byte_offset_reference
        if r.get_byte_offset() is not None:
            retval = self.__visit_byte_offset_reference(r) or r, -1
            r._reference__referenced_object = retval[0]  # type: ignore[attr-defined]
            return r.get_referenced_object()

        # default (not able to resolve)
        return r

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
        if self.get_bytes()[node] not in b"0123456789":
            return None

        # read object nr
        i: int = node
        j: int = node
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        object_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read generation number
        i = j
        if self.get_bytes()[i] not in b"0123456789":
            return None
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        generation_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read 'R'
        i = j
        if self.get_bytes()[i : i + 1] != b"R":
            return None
        i += 1

        matching_ref: typing.Optional[reference] = self.__look_up_reference(
            object_nr=object_nr, generation_nr=generation_nr
        )

        # IF the exact combination of object_nr AND generation_nr could not be found
        # THERE is no matching entry, and the reference is returned as if referring to an object not in use
        if matching_ref is None:
            return (
                reference(
                    object_nr=object_nr,
                    generation_nr=generation_nr,
                    is_in_use=False,
                    byte_offset=0,
                ),
                i,
            )

        # default
        return self.__visit_reference(matching_ref), i
