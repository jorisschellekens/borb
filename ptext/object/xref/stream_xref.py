import io
from typing import Optional

from ptext.exception.pdf_exception import PDFTypeError, PDFValueError
from ptext.io.tokenizer.high_level_tokenizer import HighLevelTokenizer
from ptext.object.pdf_high_level_object import PDFHighLevelObject
from ptext.object.xref.xref import XREF
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_boolean import PDFBoolean
from ptext.primitive.pdf_indirect_reference import PDFIndirectReference
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_number import PDFInt
from ptext.primitive.pdf_object import PDFIndirectObject
from ptext.primitive.pdf_stream import PDFStream


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

    def __init__(self, initial_offset: Optional[int] = None):
        super().__init__()
        self.initial_offset = initial_offset

    def read(
        self,
        io_source: io.IOBase,
        tokenizer: HighLevelTokenizer,
        initial_offset: Optional[int] = None,
    ) -> "PDFHighLevelObject":

        if initial_offset is not None:
            self.input.seek(initial_offset)
        else:
            self._seek_to_xref_token(io_source, tokenizer)

        xref_stream_indirect = tokenizer.read_object()
        if not isinstance(xref_stream_indirect, PDFIndirectObject):
            raise PDFTypeError(
                received_type=xref_stream_indirect.__class__,
                expected_type=PDFIndirectObject,
            )
        if not isinstance(xref_stream_indirect.get_object(), PDFStream):
            raise PDFTypeError(
                received_type=xref_stream_indirect.get_object().__class__,
                expected_type=PDFStream,
            )

        xref_stream = xref_stream_indirect.get_object()

        # check widths
        widths_name = PDFName("W")
        if widths_name not in xref_stream.stream_dictionary:
            raise PDFTypeError(expected_type=PDFArray, received_type=None)
        if any(
            [
                not isinstance(xref_stream.stream_dictionary[widths_name][x], PDFInt)
                for x in range(0, len(xref_stream.stream_dictionary[widths_name]))
            ]
        ):
            raise PDFValueError(
                expected_value_description="[PDFInt]",
                received_value_description=str(
                    [str(x) for x in xref_stream.stream_dictionary[widths_name]]
                ),
            )

        # decode widths
        widths = [
            xref_stream.stream_dictionary[widths_name][x].get_int_value()
            for x in range(0, len(xref_stream.stream_dictionary[widths_name]))
        ]
        total_entry_width = sum(widths)

        # list of references
        indirect_references = [
            PDFIndirectReference(
                object_number=PDFInt(0),
                generation_number=PDFInt(65535),
                is_in_use=PDFBoolean(False),
                document=self.document,
            )
        ]

        # check size
        if not PDFName("Size") in xref_stream.stream_dictionary:
            raise PDFTypeError(expected_type=PDFInt, received_type=None)
        if not isinstance(xref_stream.stream_dictionary[PDFName("Size")], PDFInt):
            raise PDFTypeError(
                expected_type=PDFInt,
                received_type=xref_stream.stream_dictionary[PDFName("Size")].__class__,
            )

        # get size
        number_of_objects = xref_stream.stream_dictionary[
            PDFName("Size")
        ].get_int_value()

        # index
        index_name = PDFName("Index")
        index = PDFArray()
        if index_name in xref_stream.stream_dictionary:
            index = xref_stream.stream_dictionary[index_name]
            if (
                not isinstance(index, PDFArray)
                or len(index) != 2
                or not isinstance(index[0], PDFInt)
                or not isinstance(index[1], PDFInt)
            ):
                raise PDFTypeError(
                    expected_type=[PDFInt].__class__, received_type=index.__class__
                )
        else:
            index = PDFArray().append(PDFInt(0)).append(PDFInt(number_of_objects))

        # read every range specified in \Index
        xref_stream_decoded_bytes = xref_stream.get_decoded_bytes()
        for idx in range(0, len(index), 2):
            start = index[idx].get_int_value()
            length = index[idx + 1].get_int_value()

            for i in range(0, length):
                bytes = xref_stream_decoded_bytes[
                    i * total_entry_width : (i + 1) * total_entry_width
                ]

                # object number
                object_number = start + i

                # read type
                type = 1
                if widths[0] > 0:
                    type = 0
                    for j in range(0, widths[0]):
                        type = (type << 8) + (bytes[j] & 0xFF)

                # read field 2
                field2 = 0
                for j in range(0, widths[1]):
                    field2 = (field2 << 8) + (bytes[widths[0] + j] & 0xFF)

                # read field 3
                field3 = 0
                for j in range(0, widths[2]):
                    field3 = (field3 << 8) + (bytes[widths[0] + widths[1] + j] & 0xFF)

                if type not in [0, 1, 2]:
                    raise PDFValueError(
                        expected_value_description="integer in [0, 1, 2]",
                        received_value_description=str(type),
                    )

                pdf_indirect_reference = None
                if type == 0:
                    # type      :The type of this entry, which shall be 0. Type 0 entries define
                    # the linked list of free objects (corresponding to f entries in a
                    # cross-reference table).
                    # field2    : The object number of the next free object
                    # field3    : The generation number to use if this object number is used again
                    pdf_indirect_reference = PDFIndirectReference(
                        document=self.document,
                        object_number=PDFInt(object_number),
                        byte_offset=PDFInt(field2),
                        generation_number=PDFInt(field3),
                        is_in_use=PDFBoolean(False),
                    )

                if type == 1:
                    # Type      : The type of this entry, which shall be 1. Type 1 entries define
                    # objects that are in use but are not compressed (corresponding
                    # to n entries in a cross-reference table).
                    # field2    : The byte offset of the object, starting from the beginning of the
                    # file.
                    # field3    : The generation number of the object. Default value: 0.
                    pdf_indirect_reference = PDFIndirectReference(
                        document=self.document,
                        object_number=PDFInt(object_number),
                        byte_offset=PDFInt(field2),
                        generation_number=PDFInt(field3),
                    )

                if type == 2:
                    # Type      : The type of this entry, which shall be 2. Type 2 entries define
                    # compressed objects.
                    # field2    : The object number of the object stream in which this object is
                    # stored. (The generation number of the object stream shall be
                    # implicitly 0.)
                    # field3    : The index of this object within the object stream.
                    pdf_indirect_reference = PDFIndirectReference(
                        document=self.document,
                        object_number=PDFInt(object_number),
                        generation_number=PDFInt(0),
                        parent_stream_object_number=PDFInt(field2),
                        index_in_parent_stream_object=PDFInt(field3),
                    )

                # append
                existing_indirect_ref = next(
                    iter(
                        [
                            x
                            for x in indirect_references
                            if x.object_number is not None
                            and x.object_number == PDFInt(object_number)
                        ]
                    ),
                    None,
                )
                ref_is_in_reading_state = (
                    existing_indirect_ref is not None
                    and existing_indirect_ref.is_in_use == PDFBoolean(True)
                    and existing_indirect_ref.generation_number
                    == pdf_indirect_reference.generation_number
                )
                ref_is_first_encountered = existing_indirect_ref is None or (
                    not ref_is_in_reading_state
                    and existing_indirect_ref.document is None
                )

                if ref_is_first_encountered:
                    indirect_references.append(pdf_indirect_reference)
                elif ref_is_in_reading_state:
                    existing_indirect_ref.index_in_parent_stream_object = (
                        pdf_indirect_reference.index_in_parent_stream_object
                    )
                    existing_indirect_ref.parent_stream_object_number = (
                        pdf_indirect_reference.parent_stream_object_number
                    )

        # add section
        for r in indirect_references:
            self.add_indirect_reference(r)

        # initialize trailer
        trailer = xref_stream.stream_dictionary
        self.set("Trailer", trailer)
