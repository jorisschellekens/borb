#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a CMap stream in a PDF document.

The `CMap` class encapsulates the functionality of a CMap (Character Map) stream,
which is used in PDF documents to map character codes to Unicode values or to
glyph identifiers in composite fonts. CMaps are essential for rendering text in
PDFs, particularly when dealing with non-standard character encodings or composite
fonts like Type 0 fonts.

This class extends the `stream` class, leveraging its capabilities for managing
PDF stream data, while adding specific methods and attributes for interpreting
CMap data. It supports parsing and interpreting character-to-glyph and
character-to-Unicode mappings.
"""
import typing

from borb.pdf.primitives import stream, name


class CMap(stream):
    """
    Represents a CMap stream in a PDF document.

    The `CMap` class encapsulates the functionality of a CMap (Character Map) stream,
    which is used in PDF documents to map character codes to Unicode values or to
    glyph identifiers in composite fonts. CMaps are essential for rendering text in
    PDFs, particularly when dealing with non-standard character encodings or composite
    fonts like Type 0 fonts.

    This class extends the `stream` class, leveraging its capabilities for managing
    PDF stream data, while adding specific methods and attributes for interpreting
    CMap data. It supports parsing and interpreting character-to-glyph and
    character-to-Unicode mappings.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(self, d: typing.Optional[dict] = None):
        """
        Initialize a CMap instance by parsing the bytes of the provided stream dictionary.

        The `CMap` class represents a character map (CMap) in a PDF, which defines mappings
        between character codes and Unicode values or glyph names. This constructor processes
        the stream data contained in the `Bytes` entry of the provided dictionary to interpret
        these mappings.

        :param d: A dictionary representing the stream, as defined in the PDF specification.
                  This includes the `Bytes` entry, which contains the raw stream data to be parsed.
        """
        super().__init__(d=d)
        self.__cmap_name: typing.Optional[name] = None
        self.__character_code_to_character: typing.Dict[int, str] = {}
        self.__character_to_character_code: typing.Dict[str, int] = {}

        # decode stream
        from borb.pdf.visitor.read.compression.decode_stream import decode_stream

        decode_stream(self)

        # parse
        self.__parse_cmap_bytes(self.get("DecodedBytes", b""))

    #
    # PRIVATE
    #

    def __bfchar(self, s: str) -> None:
        import re

        # e.g. <815c> <815c>
        m: typing.Optional[re.Match] = re.match(
            "(?P<arg0><[0-9abcdefABCDEF]+>) +(?P<arg1><[0-9abcdefABCDEF]+>)", s
        )
        if m is not None:
            arg0: int = int(m.group("arg0")[1:-1], 16)
            try:
                arg1: str = chr(int(m.group("arg1")[1:-1], 16))
            except:
                arg1 = "�"
            self.__character_code_to_character[arg0] = arg1
            return

        # e.g. <27> /quotesingle
        m = re.match("(?P<arg0><[0123456789abcdefABCDEF]+>) +(?P<arg1>/[a-zA-Z]+)", s)
        if m is not None:
            arg0: int = int(m.group("arg0")[1:-1], 16)  # type: ignore[no-redef]
            arg1: str = m.group("arg1")  # type: ignore[no-redef]
            # TODO
            return

    def __bfrange(self, s: str) -> None:
        # e.g. <0000> <005E> <0020>
        import re

        m: typing.Optional[re.Match] = re.match(
            "(?P<arg0><[0-9abcdefABCDEF]+>) +(?P<arg1><[0-9abcdefABCDEF]+>) +(?P<arg2><[0-9abcdefABCDEF]+>)",
            s,
        )
        if m is not None:
            arg0: int = int(m.group("arg0")[1:-1], 16)  # type: ignore[no-redef]
            arg1: int = int(m.group("arg1")[1:-1], 16)  # type: ignore[no-redef]
            arg2: int = int(m.group("arg2")[1:-1], 16)  # type: ignore[no-redef]
            for i in range(arg0, arg1 + 1):
                self.__character_code_to_character[i] = chr(arg2 + i - arg0)
        # TODO
        pass

    def __parse_cmap_bytes(self, cmap_bytes: bytes) -> None:
        import re

        lines: typing.List[str] = cmap_bytes.decode("latin1").splitlines()
        i: int = 0
        while i < len(lines):
            line: str = lines[i]

            # CMapName
            m: typing.Optional[re.Match] = re.match("/CMapName *(?P<arg>.+) +def", line)
            if m is not None:
                self.__cmap_name = m.group("arg")
                i += 1
                continue

            # Ordering
            # TODO

            # Registry
            # TODO

            # Supplement
            # TODO

            # <nr> begincodespacerange <hex> <hex> endcodespacerange
            m = re.match(
                "(?P<arg0>[0-9]+) +begincodespacerange +(?P<arg1><[0-9abcdefABCDEF]+>) +(?P<arg2><[0-9abcdefABCDEF]+>) +endcodespacerange",
                line,
            )
            if m is not None:
                i += 1
                continue

            # <nr> begincodespacerange
            m = re.match("(?P<arg>[0-9]+) begincodespacerange", line)
            if m is not None:
                j: int = i + 1  # type: ignore[no-redef]
                while j < len(lines) and lines[j] != "endcodespacerange":
                    j += 1
                i = j + 1
                continue

            # <nr> beginbfchar
            m = re.match("(?P<arg>[0-9]+) beginbfchar", line)
            if m is not None:
                j: int = i + 1  # type: ignore[no-redef]
                while j < len(lines) and lines[j] != "endbfchar":
                    self.__bfchar(lines[j])
                    j += 1
                i = j + 1
                continue

            # <nr> beginbfrange
            m = re.match("(?P<arg>[0-9]+) beginbfrange", line)
            if m is not None:
                j: int = i + 1  # type: ignore[no-redef]
                while j < len(lines) and lines[j] != "endbfrange":
                    self.__bfrange(lines[j])
                    j += 1
                i = j + 1
                continue

            # default
            i += 1

    #
    # PUBLIC
    #

    def first_character_code(self) -> int:
        """
        Retrieve the lowest character code defined in the CMap.

        This method returns the smallest character code for which a mapping
        exists in the CMap. It is useful when iterating over the range of
        character codes defined in the mapping.

        :return: The smallest character code as an integer.
        """
        return min(self.__character_code_to_character.keys())

    def get_character(self, character_code: int) -> str:
        """
        Retrieve the character corresponding to a given character code.

        This method uses the CMap's character-to-Unicode mapping to translate a
        character code into its corresponding Unicode character. It is useful for
        decoding text streams in PDF documents that rely on custom encodings or
        composite fonts.

        :param character_code: The character code to translate (an integer value).
        :return: The Unicode character corresponding to the given character code.
        """
        return self.__character_code_to_character.get(character_code, "�")

    def get_character_code(self, character: str) -> int:
        """
        Retrieve the character code corresponding to a given Unicode character.

        This method uses the CMap's Unicode-to-character-code mapping to find the
        character code associated with a specific Unicode character. It is useful for
        encoding text streams in PDF documents that rely on custom encodings or
        composite fonts.

        :param character: The Unicode character to translate (a single-character string).
        :return: The character code corresponding to the given Unicode character.
        """
        if len(self.__character_to_character_code) == 0:
            self.__character_to_character_code = {
                v: k for k, v in self.__character_code_to_character.items()
            }
        return self.__character_to_character_code.get(character, -1)

    def last_character_code(self) -> int:
        """
        Retrieve the highest character code defined in the CMap.

        This method returns the largest character code for which a mapping
        exists in the CMap. It is useful when iterating over the range of
        character codes defined in the mapping.

        :return: The largest character code as an integer.
        """
        return max(self.__character_code_to_character.keys())
