#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Beginning with PDF 1.5, cross-reference information may be stored in a cross-reference stream instead of in a
    cross-reference table.
"""
import io
import typing
from decimal import Decimal

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.pdf.xref.xref import XREF


class StreamXREF(XREF):
    """
    Beginning with PDF 1.5, cross-reference information may be stored in a cross-reference stream instead of in a
    cross-reference table. Cross-reference streams provide the following advantages:
    • A more compact representation of cross-reference information
    • The ability to access compressed objects that are stored in object streams (see 7.5.7, "Object Streams")
    and to allow new cross-reference entry types to be added in the future
    Cross-reference streams are stream objects (see 7.3.8, "Stream Objects"), and contain a dictionary and a data
    stream. Each cross-reference stream contains the information equivalent to the cross-reference table
     (see 7.5.4, "Cross-Reference Table") and trailer (see 7.5.5, "File Trailer") for one cross-reference section.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, initial_offset: typing.Optional[int] = None):
        super().__init__()
        self._initial_offset = initial_offset

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def read(
        self,
        io_source: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO],
        tokenizer: HighLevelTokenizer,
        initial_offset: typing.Optional[int] = None,
    ) -> "XREF":
        """
        This method attempts to read a stream XREF from the given io_source.
        It will either throw an exception, or return this XREF
        """

        if initial_offset is not None:
            io_source.seek(initial_offset)
        else:
            self._seek_to_xref_token(io_source, tokenizer)

        xref_stream = tokenizer.read_object()
        assert isinstance(xref_stream, Stream)

        # check widths
        assert "W" in xref_stream
        assert all(
            [
                isinstance(xref_stream["W"][x], Decimal)
                for x in range(0, len(xref_stream["W"]))
            ]
        )
        # decode widths
        widths = [int(xref_stream["W"][x]) for x in range(0, len(xref_stream["W"]))]
        total_entry_width = sum(widths)

        # parent
        document = self.get_root()

        # list of references
        indirect_references = [
            Reference(
                object_number=0,
                generation_number=65535,
                is_in_use=False,
                document=document,
            )
        ]

        # check size
        assert "Size" in xref_stream
        assert isinstance(xref_stream["Size"], Decimal)

        # get size
        number_of_objects = int(xref_stream["Size"])

        # index
        index = []
        if "Index" in xref_stream:
            index = xref_stream["Index"]
            assert isinstance(index, List)
            assert len(index) % 2 == 0
            assert isinstance(index[0], Decimal)
            assert isinstance(index[1], Decimal)
        else:
            index = [Decimal(0), Decimal(number_of_objects)]

        # apply filters
        xref_stream = decode_stream(xref_stream)

        # read every range specified in /Index
        xref_stream_decoded_bytes = xref_stream["DecodedBytes"]
        for idx in range(0, len(index), 2):
            start = int(index[idx])
            length = int(index[idx + 1])

            bptr = 0
            for i in range(0, length):
                # object number
                object_number = start + i

                # read type
                type = 1
                if widths[0] > 0:
                    type = 0
                    for j in range(0, widths[0]):
                        type = (type << 8) + (xref_stream_decoded_bytes[bptr] & 0xFF)
                        bptr += 1

                # read field 2
                field2 = 0
                for j in range(0, widths[1]):
                    field2 = (field2 << 8) + (xref_stream_decoded_bytes[bptr] & 0xFF)
                    bptr += 1

                # read field 3
                field3 = 0
                for j in range(0, widths[2]):
                    field3 = (field3 << 8) + (xref_stream_decoded_bytes[bptr] & 0xFF)
                    bptr += 1

                # check type
                assert type in [0, 1, 2]

                pdf_indirect_reference = None
                if type == 0:
                    # type      :The type of this entry, which shall be 0. Type 0 entries define
                    # the linked list of free objects (corresponding to f entries in a
                    # cross-reference table).
                    # field2    : The object number of the next free object
                    # field3    : The generation number to use if this object number is used again
                    pdf_indirect_reference = Reference(
                        document=document,
                        object_number=object_number,
                        byte_offset=field2,
                        generation_number=field3,
                        is_in_use=False,
                    )

                if type == 1:
                    # Type      : The type of this entry, which shall be 1. Type 1 entries define
                    # objects that are in use but are not compressed (corresponding
                    # to n entries in a cross-reference table).
                    # field2    : The byte offset of the object, starting from the beginning of the
                    # file.
                    # field3    : The generation number of the object. Default value: 0.
                    pdf_indirect_reference = Reference(
                        document=document,
                        object_number=object_number,
                        byte_offset=field2,
                        generation_number=field3,
                    )

                if type == 2:
                    # Type      : The type of this entry, which shall be 2. Type 2 entries define
                    # compressed objects.
                    # field2    : The object number of the object stream in which this object is
                    # stored. (The generation number of the object stream shall be
                    # implicitly 0.)
                    # field3    : The index of this object within the object stream.
                    pdf_indirect_reference = Reference(
                        document=document,
                        object_number=object_number,
                        generation_number=0,
                        parent_stream_object_number=field2,
                        index_in_parent_stream=field3,
                    )

                assert pdf_indirect_reference is not None

                # append
                existing_indirect_ref = next(
                    iter(
                        [
                            x
                            for x in indirect_references
                            if x.object_number is not None
                            and x.object_number == Decimal(object_number)
                        ]
                    ),
                    None,
                )
                ref_is_in_reading_state = (
                    existing_indirect_ref is not None
                    and existing_indirect_ref.is_in_use
                    and existing_indirect_ref.generation_number
                    == pdf_indirect_reference.generation_number
                )
                ref_is_first_encountered = existing_indirect_ref is None or (
                    not ref_is_in_reading_state
                    and existing_indirect_ref.document is None
                )

                if ref_is_first_encountered:
                    assert pdf_indirect_reference is not None
                    indirect_references.append(pdf_indirect_reference)
                elif ref_is_in_reading_state:
                    assert existing_indirect_ref is not None
                    assert pdf_indirect_reference is not None
                    existing_indirect_ref.index_in_parent_stream = (
                        pdf_indirect_reference.index_in_parent_stream
                    )
                    existing_indirect_ref.parent_stream_object_number = (
                        pdf_indirect_reference.parent_stream_object_number
                    )

        # add section
        for r in indirect_references:
            self.add(r)

        # initialize trailer
        self[Name("Trailer")] = Dictionary()
        for k, v in xref_stream.items():
            self[Name("Trailer")][k] = v
        self[Name("Trailer")].set_parent(self)

        # return
        return self
