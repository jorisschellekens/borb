import io
from typing import Optional, NamedTuple, List

from ptext.exception.pdf_exception import StartXREFTokenNotFoundError, PDFTypeError
from ptext.io.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.io.tokenize.low_level_tokenizer import TokenType
from ptext.io.tokenize.types.pdf_boolean import PDFBoolean
from ptext.io.tokenize.types.pdf_indirect_reference import PDFIndirectReference
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_null import PDFNull
from ptext.io.tokenize.types.pdf_number import PDFInt
from ptext.io.tokenize.types.pdf_object import PDFObject, PDFIndirectObject
from ptext.io.tokenize.types.pdf_stream import PDFStream
from ptext.io.transform.types import DictionaryWithParentAttribute


class XREFSection(NamedTuple):

    start_object_number: int
    number_of_objects: int
    indirect_references: List["PDFIndirectReference"]

    def __len__(self):
        return len(self.indirect_references)

    def __str__(self):
        s = str(self.start_object_number) + " " + str(self.number_of_objects) + "\n"
        for r in self.indirect_references:
            s += "%010d %07d %s\n" % (
                r.byte_offset.get_int_value() if r.byte_offset is not None else 0,
                r.generation_number.get_int_value()
                if r.generation_number is not None
                else 0,
                "n" if r.is_in_use == PDFBoolean(True) else "f",
            )
        return s


class XREF(DictionaryWithParentAttribute):
    def __init__(self):
        super(XREF, self).__init__()
        self.document = None
        self.tokenizer = None
        self.input = None
        self.sections = []

    ##
    ## LOWLEVEL IO
    ##

    def _find_backwards(
        self,
        src: io.IOBase,
        tok: HighLevelTokenizer,
        text_to_find: str,
    ) -> int:

        # length of str to check
        str_len = 1024

        # go to end of file
        src.seek(0, io.SEEK_END)
        file_length = src.tell()

        pos = file_length - str_len
        if pos < 1:
            pos = 1

        while pos > 0:
            src.seek(pos)
            bytes_near_eof = "".join([tok._next_char() for _ in range(0, str_len)])
            idx = bytes_near_eof.find(text_to_find)
            if idx >= 0:
                return pos + idx
            pos = pos - str_len + len(text_to_find)

        # raise error
        return -1

    def _seek_to_xref_token(self, src: io.IOBase, tok: HighLevelTokenizer):

        # find "startxref" text
        start_of_xref_token_byte_offset = self._find_backwards(src, tok, "startxref")
        if start_of_xref_token_byte_offset == -1:
            raise StartXREFTokenNotFoundError()

        # set tokenizer to "startxref"
        src.seek(start_of_xref_token_byte_offset)
        token = tok.next_non_comment_token()
        if token.text == "xref":
            src.seek(start_of_xref_token_byte_offset)
            return

        # if we are at startxref, we are reading the XREF table backwards
        # and we need to go back to the start of XREF
        if token.text == "startxref":
            token = tok.next_non_comment_token()
            if token.token_type != TokenType.NUMBER:
                raise InvalidNumberAfterStartXREFToken(
                    token.byte_offset, token.byte_offset + len(token.text)
                )

            start_of_xref_offset = int(token.text)
            src.seek(start_of_xref_offset)

    ##
    ## GETTERS AND SETTERS
    ##

    def add_indirect_reference(
        self, indirect_reference: PDFIndirectReference
    ) -> "XREF":
        object_number = indirect_reference.get_object_number().get_int_value()

        # modify existing section
        for section in self.sections:
            if (
                section.start_object_number
                <= object_number
                < section.start_object_number + section.number_of_objects
            ):
                section.indirect_references[
                    section.start_object_number - object_number
                ] = indirect_reference
                return self

        # append to section
        for section in self.sections:
            if (
                section.start_object_number
                <= object_number
                <= section.start_object_number + section.number_of_objects
            ):
                l = section.indirect_references
                l.append(indirect_reference)
                section_b = XREFSection(
                    start_object_number=section.start_object_number,
                    number_of_objects=section.number_of_objects + 1,
                    indirect_references=l,
                )
                self.sections.remove(section)
                self.sections.append(section_b)
                return self

        # new section
        self.sections.append(
            XREFSection(
                start_object_number=object_number,
                number_of_objects=1,
                indirect_references=[indirect_reference],
            )
        )
        return self

    def merge_references(self, other_xref: "XREF") -> "XREF":
        # sections
        for s in other_xref.sections:
            for r in s.indirect_references:
                self.add_indirect_reference(r)
        return self

    def get_indirect_reference_for_object_number(
        self, object_number: int
    ) -> Optional[PDFIndirectReference]:
        for s in self.sections:
            if (
                s.start_object_number
                <= object_number
                < s.start_object_number + s.number_of_objects
            ):
                return s.indirect_references[object_number - s.start_object_number]
        return None

    def get_object_for_indirect_reference(
        self,
        indirect_reference: PDFIndirectReference,
        src: io.IOBase,
        tok: HighLevelTokenizer,
    ) -> PDFObject:

        obj = None
        obj_number = (
            indirect_reference.object_number.get_int_value()
            if indirect_reference.object_number is not None
            else None
        )

        # lookup xref entry
        xref_entry = (
            self.get_indirect_reference_for_object_number(obj_number)
            if obj_number is not None
            else None
        )

        # reference points to an object that is not in use
        if xref_entry is not None and xref_entry.is_in_use == PDFBoolean(False):
            return PDFNull

        # object number exists, but there is no corresponding xref entry
        if obj_number is not None and xref_entry is None:
            return PDFNull

        # the indirect reference may have a byte offset
        if indirect_reference.byte_offset is not None:
            byte_offset = indirect_reference.byte_offset.get_int_value()
            tok.seek(byte_offset)
            obj = tok.read_object()

        # corresponding entry specifies a byte offset
        if xref_entry.byte_offset is not None:
            byte_offset = xref_entry.byte_offset.get_int_value()
            tok.seek(byte_offset)
            obj = tok.read_object(self)

        # entry specifies a parent object
        if xref_entry.parent_stream_object_number is not None:
            parent_ref = PDFIndirectReference(
                object_number=xref_entry.parent_stream_object_number
            )

            # read parent object
            stream_object = self.get_object_for_indirect_reference(parent_ref, src, tok)
            if not isinstance(stream_object, PDFIndirectObject) or not isinstance(
                stream_object.get_object(), PDFStream
            ):
                raise PDFTypeError(
                    expected_type=PDFStream, received_type=stream_object.__class__
                )
            first_byte = (
                stream_object.get_object()
                .stream_dictionary[PDFName("First")]
                .get_int_value()
                if PDFName("First") in stream_object.get_object().stream_dictionary
                else 0
            )
            stream_bytes = stream_object.get_object().get_decoded_bytes()[first_byte:]

            # fetch index in parent
            index = xref_entry.index_in_parent_stream_object.get_int_value()
            length = 0
            if isinstance(
                stream_object.get_object().stream_dictionary[PDFName("Length")],
                PDFIndirectReference,
            ):
                length = (
                    self.get_object_for_indirect_reference(
                        stream_object.get_object().stream_dictionary[PDFName("Length")],
                        src,
                        tok,
                    )
                    .get_object()
                    .get_int_value()
                )
            if isinstance(
                stream_object.get_object().stream_dictionary[PDFName("Length")], PDFInt
            ):
                length = (
                    stream_object.get_object()
                    .stream_dictionary[PDFName("Length")]
                    .get_int_value()
                )

            # tokenize parent stream
            if index < length:
                tok = HighLevelTokenizer(io.BytesIO(stream_bytes))
                obj = [tok.read_object() for x in range(0, index + 1)]
                obj = obj[-1]
            else:
                obj = PDFNull()

        if isinstance(obj, PDFIndirectObject):
            return obj
        else:
            return PDFIndirectObject(object=obj, indirect_reference=indirect_reference)

    ##
    ## OVERRIDES
    ##

    def __len__(self):
        return sum([len(x) for x in self.sections])

    def __str__(self):
        out = "xref\n"
        for s in self.sections:
            out += str(s)
        out += "startxref"
        return out
