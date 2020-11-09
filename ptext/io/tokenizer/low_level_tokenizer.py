import enum
import io
from typing import Optional

from ptext.exception.pdf_exception import PDFEOFError


class TokenType(enum.IntEnum):
    NUMBER = 1
    STRING = 2
    HEX_STRING = 3
    NAME = 4
    COMMENT = 5
    START_ARRAY = 6
    END_ARRAY = 7
    START_DICT = 8
    END_DICT = 9
    REF = 10
    OBJ = 11
    END_OBJ = 12
    OTHER = 13
    END_OF_FILE = 14


class Token:
    def __init__(self, byte_offset: int, token_type: TokenType, text: str):
        self.byte_offset = byte_offset
        self.token_type = token_type
        self.text = text

    def set_byte_offset(self, byte_offset: int) -> "Token":
        """
        Set the byte offset of this Token
        """
        self.byte_offset = byte_offset
        return self

    def set_text(self, text: str) -> "Token":
        """
        Set the text of this Token
        """
        self.text = text
        return self

    def set_token_type(self, token_type: TokenType) -> "Token":
        """
        Set the TokenType of this Token
        """
        self.token_type = token_type
        return self


class LowLevelTokenizer:
    def __init__(self, io_source):
        self.io_source = io_source

    def next_non_comment_token(self) -> Optional[Token]:
        t = self.next_token()
        while t is not None and t.token_type == TokenType.COMMENT:
            t = self.next_token()
        return t

    def next_token(self) -> Optional[Token]:

        ch = self._next_char()
        if len(ch) == 0:
            return None

        while len(ch) > 0 and self._is_whitespace(ch):
            ch = self._next_char()

        # START_ARRAY
        if ch == "[":
            return Token(self.io_source.tell() - 1, TokenType.START_ARRAY, "[")

        # END ARRAY
        if ch == "]":
            return Token(self.io_source.tell() - 1, TokenType.END_ARRAY, "]")

        # NAME
        if ch == "/":
            out_str = "/"
            out_pos = self.io_source.tell() - 1
            while True:
                ch = self._next_char()
                if len(ch) == 0:
                    break
                if self._is_delimiter(ch):
                    break
                out_str += ch
            if len(ch) != 0:
                self._prev_char()
            return Token(out_pos, TokenType.NAME, out_str)

        # END_DICT
        if ch == ">":
            out_pos = self.io_source.tell() - 1
            ch = self._next_char()
            # UNEXPECTED CHARACTER AFTER >
            if ch != ">":
                raise ValueError(
                    "Invalid character at byte position %d, expected >."
                    % self.io_source.tell()
                )
            return Token(out_pos, TokenType.END_DICT, ">>")

        # COMMENT
        if ch == "%":
            out_str = ""
            out_pos = self.io_source.tell() - 1
            while len(ch) != 0 and ch != "\r" and ch != "\n":
                out_str += ch
                ch = self._next_char()
            if len(ch) != 0:
                self._prev_char()
            return Token(out_pos, TokenType.COMMENT, out_str)

        # HEX_STRING OR DICT
        if ch == "<":
            out_pos = self.io_source.tell() - 1
            ch = self._next_char()

            # DICT
            if ch == "<":
                return Token(out_pos, TokenType.START_DICT, "<<")

            # empty hex string
            if ch == ">":
                return Token(out_pos, TokenType.HEX_STRING, "<>")

            # HEX_STRING
            out_str = "<" + ch
            while True:
                ch = self._next_char()
                if len(ch) == 0:
                    break
                out_str += ch
                if ch == ">":
                    break

            return Token(out_pos, TokenType.HEX_STRING, out_str)

        # NUMBER
        if ch in "-+.0123456789":
            out_str = ""
            out_pos = self.io_source.tell() - 1
            while len(ch) != 0 and ch in "-+.0123456789":
                out_str += ch
                ch = self._next_char()
            if len(ch) != 0:
                self._prev_char()
            return Token(out_pos, TokenType.NUMBER, out_str)

        # STRING
        if ch == "(":
            bracket_nesting_level = 1
            out_str = "("
            out_pos = self.io_source.tell() - 1
            while True:
                ch = self._next_char()
                if len(ch) == 0:
                    break
                if ch == "\\":
                    ch = self._next_char()
                    out_str += ch
                    continue
                if ch == "(":
                    bracket_nesting_level += 1
                if ch == ")":
                    bracket_nesting_level -= 1
                out_str += ch
                if bracket_nesting_level == 0:
                    break
            if len(ch) == 0:
                raise PDFEOFError()
            if out_str.endswith("\\"):
                raise ValueError(
                    "escape character without subsequent character at position %d."
                    % self.io_source.tell()
                )
            return Token(out_pos, TokenType.STRING, out_str)

        # OTHER
        out_str = ""
        out_pos = self.io_source.tell() - 1
        while len(ch) != 0 and not self._is_delimiter(ch):
            out_str += ch
            ch = self._next_char()
        if len(ch) != 0:
            self._prev_char()
        return Token(out_pos, TokenType.OTHER, out_str)

    def seek(self, pos: int, whence: int = io.SEEK_SET):
        """
        Change the stream position to the given byte offset. offset is interpreted relative to the position indicated by whence.
        The default value for whence is SEEK_SET. Values for whence are:
        SEEK_SET or 0 – start of the stream (the default); offset should be zero or positive
        SEEK_CUR or 1 – current stream position; offset may be negative
        SEEK_END or 2 – end of the stream; offset is usually negative
        Return the new absolute position.
        """
        return self.io_source.seek(pos, whence)

    def tell(self) -> int:
        """
        Return the current stream position.
        """
        return self.io_source.tell()

    def _get_hex_value(self, ch: str) -> Optional[int]:
        if "0" <= ch <= "9":
            return ord(ch) - ord("0")
        if "A" <= ch <= "F":
            return ord(ch) - ord("A") + 10
        if "a" <= ch <= "f":
            return ord(ch) - ord("a") + 10
        return None

    def _is_delimiter(self, ch: str) -> bool:
        return (ord(ch) + 1) in [
            0,
            1,
            10,
            11,
            13,
            14,
            33,
            38,
            41,
            42,
            48,
            61,
            63,
            92,
            94,
        ]

    def _is_whitespace(self, ch: str) -> bool:
        return ord(ch) in [0, 9, 10, 12, 13, 32]

    def _next_char(self):
        return self.io_source.read(1).decode("latin-1")

    def _prev_char(self):
        return self.io_source.seek(-1, io.SEEK_CUR)
