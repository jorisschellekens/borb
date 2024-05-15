#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains everything needed to perform low-level tokenization against PDF syntax.
Low-level tokenization aims to separate numbers, strings, names, comments, start of dictionary, start of array, etc
The high-level tokenizer will use this first pass to then build complex objects (streams, dictionaries, etc)
"""
import enum
import io
import typing


class TokenType(enum.IntEnum):
    """
    This enum represents the various kinds of Token objects the PDF parser can encounter
    """

    COMMENT = 1
    END_ARRAY = 2
    END_DICT = 3
    END_OBJ = 4
    END_OF_FILE = 5
    HEX_STRING = 6
    NAME = 7
    NUMBER = 8
    OBJ = 9
    OTHER = 10
    REF = 11
    START_ARRAY = 12
    START_DICT = 13
    STRING = 14


class Token:
    """
    This class represents a token in PDF syntax.
    A lexical token or simply token is a string with an assigned and thus identified meaning.
    It is structured as a pair consisting of a token name and an optional token value.
    The token name is a category of lexical unit.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, byte_offset: int, token_type: TokenType, bts: bytes):
        # TODO: sort args
        self._bytes: bytes = bts
        self._byte_offset: int = byte_offset
        self._token_type: TokenType = token_type

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_byte_offset(self) -> int:
        """
        Get the byte offset of this Token
        :return:    the byte offset
        """
        return self._byte_offset

    def get_bytes(self) -> bytes:
        """
        Get the bytes of this Token
        :return:    the bytes
        """
        return self._bytes

    def get_text(self, encoding: str = "latin1") -> str:
        """
        Get the text of this Token, using a given encoding (default: latin1)
        :param encoding:    the encoding to be used (default is latin1)
        :return:            the text
        """
        return self._bytes.decode(encoding)

    def get_token_type(self) -> TokenType:
        """
        Get the TokenType of this Token
        :return:    the TokenType
        """
        return self._token_type


class LowLevelTokenizer:
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

    def __init__(self, io_source):
        self._io_source = io_source
        # fmt: off
        self._is_delimiter = {b'\x00', b'\t', b'\n', b'\r', b'\x0c', b" ", b'%', b'(', b')', b'/', b'<', b'>', b'[', b']'}.__contains__
        self._is_pseudo_digit = {b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'+', b'-', b'.'}.__contains__
        self._is_whitespace = {b'\x00', b'\t', b'\n', b'\r', b'\x0c', b' '}.__contains__
        # fmt: on

    #
    # PRIVATE
    #

    def _next_byte(self):
        return self._io_source.read(1)

    def _prev_byte(self):
        return self._io_source.seek(-1, io.SEEK_CUR)

    #
    # PUBLIC
    #

    def next_non_comment_token(self) -> typing.Optional[Token]:
        """
        This function retrieves the next non-comment Token.
        It returns None if no such Token exists (end of stream/file)
        :return:    the next non-comment Token
        """
        t = self.next_token()
        while t is not None and t.get_token_type() == TokenType.COMMENT:
            t = self.next_token()
        return t

    def next_token(self) -> typing.Optional[Token]:
        """
        This function retrieves the next Token.
        It returns None if no such Token exists (end of stream/file)
        :return:    the next Token
        """
        ch = self._next_byte()
        if len(ch) == 0:
            return None

        # skip whitespace
        while len(ch) > 0 and self._is_whitespace(ch):
            ch = self._next_byte()

        # START_ARRAY
        if ch == b"[":
            return Token(self._io_source.tell() - 1, TokenType.START_ARRAY, b"[")

        # END ARRAY
        if ch == b"]":
            return Token(self._io_source.tell() - 1, TokenType.END_ARRAY, b"]")

        # NAME
        out_str: bytearray = bytearray()
        if ch == b"/":
            out_str = bytearray(b"/")
            out_pos = self._io_source.tell() - 1
            while True:
                ch = self._next_byte()
                if len(ch) == 0:
                    break
                if self._is_delimiter(ch):
                    break
                out_str += ch
            if len(ch) != 0:
                self._prev_byte()
            return Token(out_pos, TokenType.NAME, bytes(out_str))

        # END_DICT
        if ch == b">":
            out_pos = self._io_source.tell() - 1
            ch = self._next_byte()
            # CHECK UNEXPECTED CHARACTER AFTER FIRST >
            assert ch == b">", "Unexpected character at end of dictionary."
            return Token(out_pos, TokenType.END_DICT, b">>")

        # COMMENT
        if ch == b"%":
            out_str = bytearray([])
            out_pos = self._io_source.tell() - 1
            while len(ch) != 0 and ch != b"\r" and ch != b"\n":
                out_str += ch
                ch = self._next_byte()
            if len(ch) != 0:
                self._prev_byte()
            return Token(out_pos, TokenType.COMMENT, bytes(out_str))

        # HEX_STRING OR DICT
        if ch == b"<":
            out_pos = self._io_source.tell() - 1
            ch = self._next_byte()

            # DICT
            if ch == b"<":
                return Token(out_pos, TokenType.START_DICT, b"<<")

            # empty hex string
            if ch == b">":
                return Token(out_pos, TokenType.HEX_STRING, b"<>")

            # HEX_STRING
            out_str = bytearray(b"<")
            out_str += ch
            while True:
                ch = self._next_byte()
                if len(ch) == 0:
                    break
                out_str += ch
                if ch == b">":
                    break
            return Token(out_pos, TokenType.HEX_STRING, bytes(out_str))

        # NUMBER
        if self._is_pseudo_digit(ch):
            out_str = bytearray([])
            out_pos = self._io_source.tell() - 1
            while len(ch) != 0 and self._is_pseudo_digit(ch):
                out_str += ch
                ch = self._next_byte()
            if len(ch) != 0:
                self._prev_byte()
            return Token(out_pos, TokenType.NUMBER, bytes(out_str))

        # STRING
        if ch == b"(":
            bracket_nesting_level = 1
            out_str = bytearray(b"(")
            out_pos = self._io_source.tell() - 1
            while True:
                ch = self._next_byte()
                if len(ch) == 0:
                    break
                # escape char
                if ch == b"\\":
                    ch = self._next_byte()
                    out_str += b"\\"
                    out_str += ch
                    continue
                if ch == b"(":
                    bracket_nesting_level += 1
                if ch == b")":
                    bracket_nesting_level -= 1
                out_str += ch
                if bracket_nesting_level == 0:
                    break
            assert len(ch) != 0
            assert out_str[-1] != b"\\"
            return Token(out_pos, TokenType.STRING, bytes(out_str))

        # OTHER
        out_str = bytearray([])
        out_pos = self._io_source.tell() - 1
        while len(ch) != 0 and not self._is_delimiter(ch):
            out_str += ch
            ch = self._next_byte()
        if len(ch) != 0:
            self._prev_byte()
        return Token(out_pos, TokenType.OTHER, bytes(out_str))

    def seek(self, pos: int, whence: int = io.SEEK_SET):
        """
        Change the stream position to the given byte offset. offset is interpreted relative to the position indicated by whence.
        The default value for whence is SEEK_SET. Values for whence are:
        SEEK_SET or 0 – start of the stream (the default); offset should be zero or positive
        SEEK_CUR or 1 – current stream position; offset may be negative
        SEEK_END or 2 – end of the stream; offset is usually negative
        Return the new absolute position.
        :param pos:         the desired (relative) stream position
        :param whence:      how the position should be interpreted (relative to what)
        :return:            the new absolute position
        """
        return self._io_source.seek(pos, whence)

    def tell(self) -> int:
        """
        Return the current stream position.
        :return:    the current stream position
        """
        return self._io_source.tell()
