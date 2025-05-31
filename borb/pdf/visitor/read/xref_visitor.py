#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class responsible for navigating and interpreting the cross-reference (XRef) table  and trailer information in a PDF file.

The `XRefVisitor` class is designed to traverse and extract data related to the structure of a
PDF file’s cross-reference table, which maintains a directory of all objects within the file.
This visitor reads object numbers, byte offsets, and generation numbers, enabling efficient
access to each object’s position in the file. The visitor also processes the trailer dictionary,
which includes information about the document structure, such as the root object, encryption
status, and file size metadata.

`XRefVisitor` serves as a base class for specialized xref-related visitors, such as those
that handle compressed xref streams or particular cross-reference formats. It can be
extended to implement specific reading strategies or custom xref processing behaviors,
supporting robust and optimized PDF parsing.
"""
import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class XRefVisitor(ReadVisitor):
    """
    A visitor class responsible for navigating and interpreting the cross-reference (XRef) table  and trailer information in a PDF file.

    The `XRefVisitor` class is designed to traverse and extract data related to the structure of a
    PDF file’s cross-reference table, which maintains a directory of all objects within the file.
    This visitor reads object numbers, byte offsets, and generation numbers, enabling efficient
    access to each object’s position in the file. The visitor also processes the trailer dictionary,
    which includes information about the document structure, such as the root object, encryption
    status, and file size metadata.

    `XRefVisitor` serves as a base class for specialized xref-related visitors, such as those
    that handle compressed xref streams or particular cross-reference formats. It can be
    extended to implement specific reading strategies or custom xref processing behaviors,
    supporting robust and optimized PDF parsing.
    """

    __DICT_CLOSE_BRACKETS = b">>"
    __DICT_OPEN_BRACKETS = b"<<"
    __SPACE = b" "

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _get_matching_dictionary_close(self, start_of_dictionary_pos: int) -> int:
        end_of_dictionary_pos: int = start_of_dictionary_pos + 2
        dict_nesting_level: int = 1
        while end_of_dictionary_pos < len(self.get_bytes()) and dict_nesting_level != 0:
            if (
                self.get_bytes()[end_of_dictionary_pos : end_of_dictionary_pos + 2]
                == XRefVisitor.__DICT_OPEN_BRACKETS
            ):
                dict_nesting_level += 1
                end_of_dictionary_pos += 2
                continue
            if (
                self.get_bytes()[end_of_dictionary_pos : end_of_dictionary_pos + 2]
                == XRefVisitor.__DICT_CLOSE_BRACKETS
            ):
                dict_nesting_level -= 1
                end_of_dictionary_pos += 2
                continue
            end_of_dictionary_pos += 1
        return end_of_dictionary_pos

    def _get_value_from_dictionary_bytes(
        self,
        from_byte: int,
        to_byte: int,
        key: bytes,
        default_value: typing.Any = None,
    ) -> typing.Optional[PDFType]:
        # IF the key does not start with a leading /
        # THEN change the key
        if not key.startswith(b"/"):
            key = b"/" + key

        # IF the key was not found
        # THEN return None
        index_of_key: int = self.get_bytes().find(key, from_byte, to_byte)
        if index_of_key == -1:
            return default_value

        # skip any spaces/newlines following /Type
        i: int = index_of_key + len(key)
        skipped_space: bool = True
        while skipped_space:
            skipped_space = False
            if self.get_bytes()[i : i + 1] == XRefVisitor.__SPACE:
                i += 1
                skipped_space = True
                continue
            if self.get_bytes()[i : i + 2] == b"\n\r":
                i += 2
                skipped_space = True
            if self.get_bytes()[i : i + 2] == b"\r\n":
                i += 2
                skipped_space = True
            if self.get_bytes()[i : i + 1] == b"\n":
                i += 1
                skipped_space = True
            if self.get_bytes()[i : i + 1] == b"\r":
                i += 1
                skipped_space = True

        try:
            retval_and_i = self.root_generic_visit(i)
            if retval_and_i is None:
                return default_value
            return retval_and_i[0]
        except:
            return default_value

    #
    # PUBLIC
    #
