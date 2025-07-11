#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for processing compressed cross-reference (XRef) tables in a PDF.

The `CompressedXRefVisitor` class extends `ReadVisitor` and is responsible for
reading and interpreting compressed XRef tables in PDF files. Compressed XRefs
store references to PDF objects in a more compact form than traditional
uncompressed XRef tables, and are commonly used in newer PDF versions to reduce
file size.

This visitor identifies and processes the compressed XRef structure, extracting
and mapping object locations for later retrieval during document parsing. It
traverses the PDF structure to locate and interpret object information, aiding
in building the PDF object tree for decoding and rendering purposes.
"""
import typing

from borb.pdf.primitives import stream, name, reference
from borb.pdf.visitor.read.compression.decode_stream import decode_stream
from borb.pdf.visitor.read.xref_visitor import XRefVisitor


class CompressedXRefVisitor(XRefVisitor):
    """
    Visitor class for processing compressed cross-reference (XRef) tables in a PDF.

    The `CompressedXRefVisitor` class extends `ReadVisitor` and is responsible for
    reading and interpreting compressed XRef tables in PDF files. Compressed XRefs
    store references to PDF objects in a more compact form than traditional
    uncompressed XRef tables, and are commonly used in newer PDF versions to reduce
    file size.

    This visitor identifies and processes the compressed XRef structure, extracting
    and mapping object locations for later retrieval during document parsing. It
    traverses the PDF structure to locate and interpret object information, aiding
    in building the PDF object tree for decoding and rendering purposes.
    """

    __DICT_OPEN_BRACKETS = b"<<"

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
        if not isinstance(node, int):
            return None
        if (
            self.get_bytes()[node : node + 2]
            != CompressedXRefVisitor.__DICT_OPEN_BRACKETS
        ):
            return None

        start_of_xref_dict: int = node
        end_of_xref_dict: int = self._get_matching_dictionary_close(
            start_of_dictionary_pos=start_of_xref_dict
        )

        if (
            self._get_value_from_dictionary_bytes(
                from_byte=start_of_xref_dict, to_byte=end_of_xref_dict, key=b"Type"
            )
            != "XRef"
        ):
            return None

        # read newline (\n\r)
        i: int = end_of_xref_dict
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read 'stream'
        has_seen_stream: bool = False
        if self.get_bytes()[i : i + 6] == b"stream":
            has_seen_stream = True
            i += 6

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read the bytes of the stream
        length = self._get_value_from_dictionary_bytes(
            from_byte=start_of_xref_dict, to_byte=end_of_xref_dict, key=b"Length"
        )
        assert isinstance(length, int)
        stream_bytes: bytes = self.get_bytes()[i : i + length]
        i += length

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read 'endstream'
        has_seen_endstream: bool = False
        if self.get_bytes()[i : i + 9] == b"endstream":
            has_seen_endstream = True
            i += 9

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read params to decode compressed xref stream
        decode_params = self._get_value_from_dictionary_bytes(
            from_byte=start_of_xref_dict,
            to_byte=end_of_xref_dict,
            key=b"DecodeParms",
            default_value={},
        )
        filter = self._get_value_from_dictionary_bytes(
            from_byte=start_of_xref_dict, to_byte=end_of_xref_dict, key=b"Filter"
        )
        assert isinstance(filter, str) or isinstance(filter, list)
        size = self._get_value_from_dictionary_bytes(
            from_byte=start_of_xref_dict, to_byte=end_of_xref_dict, key=b"Size"
        )
        assert isinstance(size, int)
        indices = self._get_value_from_dictionary_bytes(
            from_byte=start_of_xref_dict,
            to_byte=end_of_xref_dict,
            key=b"Index",
            default_value=[0, size],
        )
        assert isinstance(indices, list)
        widths = self._get_value_from_dictionary_bytes(
            from_byte=start_of_xref_dict, to_byte=end_of_xref_dict, key=b"W"
        )
        assert isinstance(widths, list)
        assert isinstance(widths[0], int)
        assert isinstance(widths[1], int)
        assert isinstance(widths[2], int)

        # decode the entire stream
        tmp_stream: stream = decode_stream(
            stream(
                {
                    name("Bytes"): stream_bytes,
                    name("DecodeParms"): decode_params,
                    name("Filter"): filter,
                    name("Length"): length,
                }
            )
        )

        # process decoded bytes
        decoded_xref_bytes: bytes = tmp_stream["DecodedBytes"]
        xref: typing.List[reference] = []
        for k in range(0, len(indices), 2):
            start = indices[k]
            length = indices[k + 1]
            assert isinstance(start, int)
            assert isinstance(length, int)

            # Each entry in a cross-reference stream shall have one or more fields, the first of which designates the entry’s
            # type (see Table 18). In PDF 1.5 through PDF 1.7, only types 0, 1, and 2 are allowed. Any other value shall be
            # interpreted as a reference to the null object, thus permitting new entry types to be defined in the future.

            decoded_xref_byte_pointer: int = 0
            for l in range(0, length):

                # object number
                object_number: int = start + l

                # read type
                field_1 = 1
                if widths[0] > 0:
                    field_1 = 0
                    for j in range(0, widths[0]):
                        field_1 = (field_1 << 8) + (
                            decoded_xref_bytes[decoded_xref_byte_pointer] & 0xFF
                        )
                        decoded_xref_byte_pointer += 1
                assert field_1 in [0, 1, 2]

                # read field 2
                field_2 = 0
                for j in range(0, widths[1]):
                    field_2 = (field_2 << 8) + (
                        decoded_xref_bytes[decoded_xref_byte_pointer] & 0xFF
                    )
                    decoded_xref_byte_pointer += 1

                # read field 3
                field_3 = 0
                for j in range(0, widths[2]):
                    field_3 = (field_3 << 8) + (
                        decoded_xref_bytes[decoded_xref_byte_pointer] & 0xFF
                    )
                    decoded_xref_byte_pointer += 1

                # The type of this entry, which shall be 0. Type 0 entries define
                # the linked list of free objects (corresponding to f entries in a
                # cross-reference table).
                if field_1 == 0:
                    ref = reference(
                        object_nr=object_number,
                        byte_offset=field_2,
                        generation_nr=field_3,
                        is_in_use=False,
                    )
                    xref += [ref]

                # The type of this entry, which shall be 1. Type 1 entries define
                # objects that are in use but are not compressed (corresponding
                # to n entries in a cross-reference table).
                if field_1 == 1:
                    ref = reference(
                        object_nr=object_number,
                        byte_offset=field_2,
                        generation_nr=field_3,
                    )
                    xref += [ref]

                # The type of this entry, which shall be 2. Type 2 entries define
                # compressed objects.
                if field_1 == 2:
                    ref = reference(
                        object_nr=object_number,
                        generation_nr=0,
                        parent_stream_object_nr=field_2,
                        index_in_parent_stream=field_3,
                    )
                    xref += [ref]

        # for every entry that refers to a parent stream
        # set the byte offset
        for ref in xref:
            if ref.get_parent_stream_object_nr() is not None:
                ref.__byte_offset = next(
                    iter(
                        [
                            x.get_byte_offset()
                            for x in xref[::-1]
                            if x.get_object_nr() == ref.get_parent_stream_object_nr()
                        ]
                    )
                )

        # add to (root) xref tables
        self._ReadVisitor__root._RootVisitor__xref += xref  # type: ignore[attr-defined]

        # IF the /Prev key has been set
        # THEN process the previous xref as well
        # fmt: off
        prev = self._get_value_from_dictionary_bytes(from_byte=start_of_xref_dict,
                                                                           to_byte=end_of_xref_dict,
                                                                           key=b"Prev",
                                                                           default_value=None)
        if prev is not None:
            assert isinstance(prev, int)
            self.root_generic_visit(prev)
        # fmt: on

        # return
        return xref, i
