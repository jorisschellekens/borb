#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The cross-reference table contains information that permits random access to indirect objects within the file so
    that the entire file need not be read to locate any particular object.
"""
import io
import typing

from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.tokenize.low_level_tokenizer import TokenType
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.pdf.xref.xref import XREF


class PlainTextXREF(XREF):
    """
    The cross-reference table contains information that permits random access to indirect objects within the file so
    that the entire file need not be read to locate any particular object. The table shall contain a one-line entry for
    each indirect object, specifying the byte offset of that object within the body of the file. (Beginning with PDF 1.5,
    some or all of the cross-reference information may alternatively be contained in cross-reference streams; see
    7.5.8, "Cross-Reference Streams.")

    NOTE 1
    The cross-reference table is the only part of a PDF file with a fixed format, which permits entries in the table to
    be accessed randomly.
    The table comprises one or more cross-reference sections. Initially, the entire table consists of a single section
    (or two sections if the file is linearized; see Annex F). One additional section shall be added each time the file is
    incrementally updated (see 7.5.6, "Incremental Updates").

    Each cross-reference section shall begin with a line containing the keyword xref. Following this line shall be
    one or more cross-reference subsections, which may appear in any order. For a file that has never been
    incrementally updated, the cross-reference section shall contain only one subsection, whose object numbering
    begins at 0.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__()

    #
    # PRIVATE
    #

    def _read_section(
        self,
        src: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO],
        tok: HighLevelTokenizer,
    ) -> typing.List[Reference]:
        tokens = [tok.next_non_comment_token() for _ in range(0, 2)]
        assert tokens[0] is not None
        assert tokens[1] is not None
        if tokens[0].get_text() in ["trailer", "startxref"]:
            src.seek(tokens[0].get_byte_offset())
            return []
        assert tokens[0].get_token_type() == TokenType.NUMBER
        assert tokens[1].get_token_type() == TokenType.NUMBER

        start_object_number = int(tokens[0].get_text())
        number_of_objects = int(tokens[1].get_text())
        indirect_references = []

        # read subsection
        for i in range(0, number_of_objects):
            tokens = [tok.next_non_comment_token() for _ in range(0, 3)]
            assert tokens[0] is not None
            assert tokens[0].get_text() not in ["trailer", "startxref"]
            assert tokens[0].get_token_type() == TokenType.NUMBER

            assert tokens[1] is not None
            assert tokens[1].get_token_type() == TokenType.NUMBER

            assert tokens[2] is not None
            assert tokens[2].get_token_type() == TokenType.OTHER
            assert tokens[2].get_text() in ["f", "n"]

            indirect_references.append(
                Reference(
                    object_number=start_object_number + i,
                    byte_offset=int(tokens[0].get_text()),
                    generation_number=int(tokens[1].get_text()),
                    is_in_use=(tokens[2].get_text() == "n"),
                )
            )

        # return
        return indirect_references

    def _read_trailer(
        self,
        src: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO],
        tok: HighLevelTokenizer,
    ) -> Dictionary:
        # return None if there is no trailer
        token = tok.next_non_comment_token()
        assert token is not None
        if token.get_text() != "trailer":
            return Dictionary()

        # if there is a keyword "trailer" the next token should be TokenType.START_DICT
        token = tok.next_non_comment_token()
        assert token is not None
        assert token.get_token_type() == TokenType.START_DICT

        # go back 2 chars "<<"
        src.seek(-2, io.SEEK_CUR)

        # read dictionary as trailer
        trailer_dict = tok.read_dictionary()

        # process startxref
        token = tok.next_non_comment_token()
        assert token is not None
        assert token.get_token_type() == TokenType.OTHER
        assert token.get_text() == "startxref"

        # return
        return trailer_dict

    #
    # PUBLIC
    #

    def read(
        self,
        src: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO],
        tok: HighLevelTokenizer,
        initial_offset: typing.Optional[int] = None,
    ) -> "XREF":
        """
        This method attempts to read a plaintext XREF from the given io_source.
        It will either throw an exception, or return this XREF
        """

        if initial_offset is not None:
            src.seek(initial_offset)
        else:
            self._seek_to_xref_token(src, tok)

        # now we should be back to the start of XREF
        token = tok.next_non_comment_token()
        assert token is not None
        assert token.get_text() == "xref"

        # read xref sections
        while True:
            xref_section = self._read_section(src, tok)
            if len(xref_section) == 0:
                break
            else:
                for r in xref_section:
                    self.add(r)

        # process trailer
        self[Name("Trailer")] = self._read_trailer(src, tok)
        self[Name("Trailer")].set_parent(self)

        # return self
        return self
