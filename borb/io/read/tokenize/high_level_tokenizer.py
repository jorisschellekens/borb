#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains everything needed to perform low-level tokenization against PDF syntax.
Low-level tokenization aims to separate numbers, strings, names, comments, start of dictionary, start of array, etc
The high-level tokenizer will use this first pass to then build complex objects (streams, dictionaries, etc)
"""
import re
import typing

from borb.io.read.tokenize.low_level_tokenizer import LowLevelTokenizer
from borb.io.read.tokenize.low_level_tokenizer import TokenType
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Boolean
from borb.io.read.types import CanvasOperatorName
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import HexadecimalString
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.read.types import String


class HighLevelTokenizer(LowLevelTokenizer):
    """
    In computer science, lexical analysis, lexing or tokenization is the process of converting a sequence of characters
    (such as in a computer program or web page) into a sequence of tokens (strings with an assigned and thus identified meaning).
    A program that performs lexical analysis may be termed a lexer, tokenizer, or scanner,
    although scanner is also a term for the first stage of a lexer.
    A lexer is generally combined with a parser, which together analyze the syntax of programming languages, web pages,
    and so forth.
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

    def read_array(self) -> List:
        """
        This function processes the next tokens and returns a List.
        It fails and throws various errors if the next tokens do not represent a List.
        :return:    a List
        """
        token = self.next_non_comment_token()
        assert token is not None
        assert token.get_token_type() == TokenType.START_ARRAY
        out = List()

        while True:
            token = self.next_non_comment_token()
            assert token is not None
            if token.get_token_type() == TokenType.END_ARRAY:
                break
            assert token.get_token_type() != TokenType.END_DICT

            # go back
            self.seek(token.get_byte_offset())

            # read
            obj = self.read_object()

            # append
            out.append(obj)

        # return
        return out

    def read_dictionary(self) -> Dictionary:
        """
        This function processes the next tokens and returns a Dictionary.
        It fails and throws various errors if the next tokens do not represent a Dictionary.
        :return:    a Dictionary
        """
        token = self.next_non_comment_token()
        assert token is not None
        assert token.get_token_type() == TokenType.START_DICT

        out_dict = Dictionary()
        while True:
            # attempt to read name token
            token = self.next_non_comment_token()
            assert token is not None
            if token.get_token_type() == TokenType.END_DICT:
                break
            assert token.get_token_type() == TokenType.NAME

            # store name
            name = Name(token.get_text()[1:])

            # attempt to read value
            value = self.read_object()
            assert value is not None

            # store in dict object
            if name is not None:
                out_dict[name] = value

        return out_dict

    def read_indirect_object(self) -> typing.Optional[AnyPDFType]:
        """
        This function processes the next tokens and returns an AnyPDFType.
        It fails and throws various errors if the next tokens do not represent an indirect pdf object.
        :return:    an (indirect) PDF object
        """

        # read object number
        token = self.next_non_comment_token()
        assert token is not None
        byte_offset = token.get_byte_offset()
        if token.get_token_type() != TokenType.NUMBER or not re.match(
            "^[0-9]+$", token.get_text()
        ):
            self.seek(byte_offset)
            return None
        object_number = int(token.get_text())

        # read generation number
        token = self.next_non_comment_token()
        assert token is not None
        if token.get_token_type() != TokenType.NUMBER or not re.match(
            "^[0-9]+$", token.get_text()
        ):
            self.seek(byte_offset)
            return None
        generation_number = int(token.get_text())

        # read 'obj'
        token = self.next_non_comment_token()
        assert token is not None
        if token.get_token_type() != TokenType.OTHER or token.get_text() != "obj":
            self.seek(byte_offset)
            return None

        # read obj
        value = self.read_object()
        if value is not None:
            value.set_reference(
                Reference(
                    object_number=object_number, generation_number=generation_number
                )
            )

        # return
        return value

    def read_indirect_reference(self) -> typing.Optional[Reference]:
        """
        This function processes the next tokens and returns an indirect reference.
        It fails and throws various errors if the next tokens do not represent an indirect reference.
        :return:    an indirect Reference
        """

        # read object number
        token = self.next_non_comment_token()
        assert token is not None
        byte_offset = token.get_byte_offset()
        if token.get_token_type() != TokenType.NUMBER or not re.match(
            "^[0-9]+$", token.get_text()
        ):
            self.seek(byte_offset)
            return None
        object_number = int(token.get_text())

        # read generation number
        token = self.next_non_comment_token()
        assert token is not None
        if token.get_token_type() != TokenType.NUMBER or not re.match(
            "^[0-9]+$", token.get_text()
        ):
            self.seek(byte_offset)
            return None
        generation_number = int(token.get_text())

        # read 'R'
        token = self.next_non_comment_token()
        assert token is not None
        if token.get_token_type() != TokenType.OTHER or token.get_text() != "R":
            self.seek(byte_offset)
            return None

        # return
        return Reference(
            object_number=object_number,
            generation_number=generation_number,
        )

    def read_object(self, xref: typing.Optional["XREF"] = None) -> typing.Optional[AnyPDFType]:  # type: ignore[name-defined]
        """
        This function processes the next tokens and returns an AnyPDFType.
        It fails and throws various errors if the next tokens do not represent a pdf object.
        :param xref:    the XREF table
        :return:        a PDF Object
        """
        token = self.next_non_comment_token()
        if token is None or len(token.get_text()) == 0:
            return None

        if token.get_token_type() == TokenType.START_DICT:
            self.seek(token.get_byte_offset())  # go to start of dictionary
            return self.read_dictionary()

        if token.get_token_type() == TokenType.START_ARRAY:
            self.seek(token.get_byte_offset())  # go to start of array
            return self.read_array()

        # <number> <number> "R"
        if token.get_token_type() == TokenType.NUMBER:
            self.seek(token.get_byte_offset())  # go to start of indirect reference
            potential_indirect_reference = self.read_indirect_reference()
            if potential_indirect_reference is not None:
                return potential_indirect_reference

        # <number> <number> "obj"
        # <<dictionary>>
        # "stream"
        # <bytes>
        # "endstream"
        if token.get_token_type() == TokenType.NUMBER:
            self.seek(token.get_byte_offset())
            potential_stream = self.read_stream(xref)
            if potential_stream is not None:
                return potential_stream

        # <number> <number> "obj"
        if token.get_token_type() == TokenType.NUMBER:
            self.seek(token.get_byte_offset())
            potential_indirect_object = self.read_indirect_object()
            if potential_indirect_object is not None:
                return potential_indirect_object

        # numbers
        if token.get_token_type() == TokenType.NUMBER:
            self.seek(self.tell() + len(token.get_text()))
            return bDecimal(token.get_text())

        # boolean
        if token.get_token_type() == TokenType.OTHER and token.get_text() in [
            "true",
            "false",
        ]:
            return Boolean(token.get_text() == "true")

        # canvas operators
        if (
            token.get_token_type() == TokenType.OTHER
            and token.get_text() in CanvasOperatorName.VALID_NAMES
        ):
            return CanvasOperatorName(token.get_text())

        # names
        if token.get_token_type() == TokenType.NAME:
            return Name(token.get_text()[1:])

        # literal strings and hex strings
        if token.get_token_type() in [TokenType.STRING, TokenType.HEX_STRING]:
            if token.get_token_type() == TokenType.STRING:
                # TODO: we should pass the bytes rather than the text
                return String(token.get_text()[1:-1])
            else:
                return HexadecimalString(token.get_text()[1:-1])

        # default
        return None

    def read_stream(self, xref: typing.Optional["XREF"] = None) -> typing.Optional[Stream]:  # type: ignore[name-defined]
        """
        This function processes the next tokens and returns a Stream.
        It fails and throws various errors if the next tokens do not represent a Stream.
        :param xref:    the XREF table
        :return:        a Stream
        """
        byte_offset = self.tell()

        # attempt to read <number> <number> obj
        # followed by dictionary
        stream_dictionary = self.read_indirect_object()
        if stream_dictionary is None or not isinstance(stream_dictionary, dict):
            self.seek(byte_offset)
            return None

        # attempt to read keyword "stream"
        stream_token = self.next_non_comment_token()
        assert stream_token is not None
        if (
            stream_token.get_token_type() != TokenType.OTHER
            or stream_token.get_text() != "stream"
        ):
            self.seek(byte_offset)
            return None

        # process /Length
        assert "Length" in stream_dictionary
        length_of_stream = stream_dictionary["Length"]
        if isinstance(length_of_stream, Reference):
            if xref is None:
                raise RuntimeError(
                    "unable to process reference /Length when no XREF is given"
                )
            pos_before = self.tell()
            length_of_stream = int(
                xref.get_object(length_of_stream, src=self._io_source, tok=self)
            )
            self.seek(pos_before)

        # process newline
        ch = self._next_byte()
        assert ch in [b"\r", b"\n"]
        if ch == b"\r":
            ch = self._next_byte()
            assert ch == b"\n"

        bytes = self._io_source.read(int(length_of_stream))

        # attempt to read token "endstream"
        end_of_stream_token = self.next_non_comment_token()
        assert end_of_stream_token is not None
        assert end_of_stream_token.get_token_type() == TokenType.OTHER
        assert end_of_stream_token.get_text() == "endstream"

        # set Bytes
        stream_dictionary[Name("Bytes")] = bytes

        # return
        output: Stream = Stream()
        for k, v in stream_dictionary.items():
            output[k] = v
        return output
