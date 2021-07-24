#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Xref tables are part of the original PDF file specification
    and one of the features which gives the PDF file format its flexibility.
    A PDF consists of lots of objects and this tells you where they are located in the file.
    This is actually very useful, as a PDF Reader just has to read these values
    and then it loads the objects only when they are needed.
    It does not need to parse or load the whole file.
"""
import io
import logging
import typing
from decimal import Decimal
from typing import Optional, Union

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.tokenize.low_level_tokenizer import TokenType
from borb.io.read.types import AnyPDFType, Dictionary, Name, Reference, Stream

logger = logging.getLogger(__name__)


class XREF(Dictionary):
    """
    Xref tables are part of the original PDF file specification
    and one of the features which gives the PDF file format its flexibility.
    A PDF consists of lots of objects and this tells you where they are located in the file.
    This is actually very useful, as a PDF Reader just has to read these values
    and then it loads the objects only when they are needed.
    It does not need to parse or load the whole file.
    """

    def __init__(self):
        super(XREF, self).__init__()
        self._entries: typing.List[Reference] = []
        self._cache: typing.Dict[int, Union[AnyPDFType, None]] = {}

    ##
    ## LOWLEVEL IO
    ##

    def _find_backwards(
        self,
        src: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO],
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

    def _seek_to_xref_token(
        self,
        src: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO],
        tok: HighLevelTokenizer,
    ):

        # find "startxref" text
        start_of_xref_token_byte_offset = self._find_backwards(src, tok, "startxref")
        assert start_of_xref_token_byte_offset is not None
        assert start_of_xref_token_byte_offset != -1

        # set tokenizer to "startxref"
        src.seek(start_of_xref_token_byte_offset)
        token = tok.next_non_comment_token()
        assert token is not None
        if token.get_text() == "xref":
            src.seek(start_of_xref_token_byte_offset)
            return

        # if we are at startxref, we are reading the XREF table backwards
        # and we need to go back to the start of XREF
        if token.get_text() == "startxref":
            token = tok.next_non_comment_token()
            assert token is not None
            assert token.get_token_type() == TokenType.NUMBER
            start_of_xref_offset = int(token.get_text())
            src.seek(start_of_xref_offset)

    ##
    ## GETTERS AND SETTERS
    ##

    def append(self, r: Reference) -> "XREF":
        """
        Add a new Reference to this XREF
        """
        self._entries.append(r)
        return self

    def merge(self, other_xref: "XREF") -> "XREF":
        """
        Merge this XREF with another XREF
        """
        for r in other_xref._entries:
            duplicate_entries = []
            if r.object_number is not None:
                duplicate_entries = [
                    x for x in self._entries if x.object_number == r.object_number
                ]
            elif r.parent_stream_object_number is not None:
                duplicate_entries = [
                    x
                    for x in self._entries
                    if x.parent_stream_object_number == r.parent_stream_object_number
                    and x.index_in_parent_stream == r.index_in_parent_stream
                ]
            if len(duplicate_entries) == 0:
                self.append(r)
        return self

    def get_object(
        self,
        indirect_reference: Union[Reference, int],
        src: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO],
        tok: HighLevelTokenizer,
    ) -> Optional[AnyPDFType]:
        """
        This function looks up an object in this XREF table.
        Objects can be looked up by Reference, or object number.
        """
        # cache
        if (
            isinstance(indirect_reference, Reference)
            and indirect_reference.parent_stream_object_number is None
        ):
            assert indirect_reference.object_number is not None
            cached_obj = self._cache.get(indirect_reference.object_number, None)
            if cached_obj is not None:
                return cached_obj

        # lookup Reference object for int
        obj = None
        if isinstance(indirect_reference, int) or isinstance(
            indirect_reference, Decimal
        ):
            refs = [
                x for x in self._entries if x.object_number == int(indirect_reference)
            ]
            if len(refs) == 0:
                return None
            indirect_reference = refs[0]

        # lookup Reference (in self) for Reference
        elif isinstance(indirect_reference, Reference):
            refs = [
                x
                for x in self._entries
                if x.object_number == indirect_reference.object_number
            ]
            if len(refs) == 0:
                return None
            indirect_reference = refs[0]

        # reference points to an object that is not in use
        assert isinstance(indirect_reference, Reference)
        if not indirect_reference.is_in_use:
            obj = None

        # the indirect reference may have a byte offset
        if indirect_reference.byte_offset is not None:
            byte_offset = int(indirect_reference.byte_offset)
            tell_before = tok.tell()
            tok.seek(byte_offset)
            obj = tok.read_object(xref=self)
            tok.seek(tell_before)

        # entry specifies a parent object
        if (
            indirect_reference.parent_stream_object_number is not None
            and indirect_reference.index_in_parent_stream is not None
        ):

            stream_object = self.get_object(
                indirect_reference.parent_stream_object_number, src, tok
            )
            assert isinstance(stream_object, Stream)
            assert "Length" in stream_object
            assert "First" in stream_object

            # Length may be Reference
            if isinstance(stream_object["Length"], Reference):
                stream_object[Name("Length")] = self.get_object(
                    stream_object["Length"], src=src, tok=tok
                )

            # First may be Reference
            if isinstance(stream_object["First"], Reference):
                stream_object[Name("First")] = self.get_object(
                    stream_object["First"], src=src, tok=tok
                )

            first_byte = int(stream_object.get("First", 0))
            if "DecodedBytes" not in stream_object:
                try:
                    stream_object = decode_stream(stream_object)
                except Exception as ex:
                    logger.debug(
                        "unable to inflate stream for object %d"
                        % indirect_reference.parent_stream_object_number
                    )
                    raise ex
            stream_bytes = stream_object["DecodedBytes"][first_byte:]

            # tokenize parent stream
            index = int(indirect_reference.index_in_parent_stream)
            length = int(stream_object["Length"])
            if index < length:
                tok = HighLevelTokenizer(io.BytesIO(stream_bytes))
                list_of_objs = [tok.read_object() for x in range(0, index + 1)]
                obj = list_of_objs[-1]
            else:
                obj = None

        # update cache
        if indirect_reference.parent_stream_object_number is None:
            assert indirect_reference.object_number is not None
            self._cache[indirect_reference.object_number] = obj

        # return
        return obj

    ##
    ## OVERRIDES
    ##

    def __len__(self):
        return len(self._entries)

    def __str__(self):
        out = "xref\n"
        for s in self.sections:
            out += str(s)
        out += "startxref"
        return out
