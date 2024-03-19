#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In metal typesetting, a font was a particular size, weight and style of a typeface.
Each font was a matched set of type, one piece (called a "sort") for each glyph, and a typeface consisting of a range of fonts that shared an overall design.

In modern usage, with the advent of digital typography, "font" is frequently synonymous with "typeface".
Each style is in a separate "font file"—for instance, the typeface "Bulmer" may include the fonts "Bulmer roman",
"Bulmer", "Bulmer bold" and "Bulmer extended"—but the term "font" might be applied either to one of these alone or to the whole typeface.

In both traditional typesetting and modern usage, the word "font" refers to the delivery mechanism of the typeface design.
In traditional typesetting, the font would be made from metal or wood.
Today, the font is a digital file.
"""
import copy
import io
import typing
from decimal import Decimal

from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.tokenize.low_level_tokenizer import Token
from borb.io.read.tokenize.low_level_tokenizer import TokenType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name


class Font(Dictionary):
    """
    In both traditional typesetting and modern usage, the word "font" refers to the delivery mechanism of the typeface design.
    In traditional typesetting, the font would be made from metal or wood.
    Today, the font is a digital file.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}) -> "Font":
        out: Font = self._empty_copy()
        # Type
        out[Name("Type")] = Name("Font")
        # BaseFont
        if "BaseFont" in self:
            out[Name("BaseFont")] = Name(str(self["BaseFont"]))
        # FirstChar
        if "FirstChar" in self:
            out[Name("FirstChar")] = self["FirstChar"]
        # LastChar
        if "LastChar" in self:
            out[Name("LastChar")] = self["LastChar"]
        # Widths
        if "Widths" in self:
            out[Name("Widths")] = List()
            for k in self["Widths"]:
                out[Name("Widths")].append(k)
        # FontDescriptor
        if "FontDescriptor" in self:
            out[Name("FontDescriptor")] = self._copy_font_descriptor(
                self["FontDescriptor"]
            )
        # Encoding
        if "Encoding" in self:
            # Name
            if isinstance(self["Encoding"], Name):
                out[Name("Encoding")] = Name(str(self["Encoding"]))
            # Dictionary
            if isinstance(self["Encoding"], Dictionary):
                out[Name("Encoding")] = Dictionary()
                out["Encoding"][Name("Type")] = Name("Encoding")
                if "BaseEncoding" in self["Encoding"]:
                    out["Encoding"][Name("BaseEncoding")] = Name(
                        str(self["Encoding"]["BaseEncoding"])
                    )
                if "Differences" in self["Encoding"]:
                    l = List()
                    for x in self["Encoding"]["Differences"]:
                        l.append(x)
                    out["Encoding"][Name("Differences")] = l
        # ToUnicode
        if "ToUnicode" in self:
            out[Name("ToUnicode")] = copy.deepcopy(self["ToUnicode"])
        # FontBBox
        if "FontBBox" in self:
            out[Name("FontBBox")] = List()
            for x in self["FontBBox"]:
                out["FontBBox"].append(x)
        # FontMatrix
        if "FontMatrix" in self:
            out[Name("FontMatrix")] = List()
            for x in self["FontMatrix"]:
                out["FontMatrix"].append(x)
        # CharProcs
        # Resources
        # CIDSystemInfo
        if "CIDSystemInfo" in self:
            out[Name("CIDSystemInfo")] = Dictionary()
            out["CIDSystemInfo"][Name("Registry")] = self["CIDSystemInfo"]["Registry"]
            out["CIDSystemInfo"][Name("Ordering")] = self["CIDSystemInfo"]["Ordering"]
            out["CIDSystemInfo"][Name("Supplement")] = self["CIDSystemInfo"][
                "Supplement"
            ]
        # DW
        if "DW" in self:
            out[Name("DW")] = self["DW"]
        # W
        if "W" in self:
            out[Name("W")] = List()
            for x in self["W"]:
                if isinstance(x, bDecimal):
                    out["W"].append(x)
                if isinstance(x, List):
                    l = List()
                    for y in x:
                        l.append(y)
                    out["W"].append(l)
        # DescendantFonts
        if "DescendantFonts" in self:
            out[Name("DescendantFonts")] = List()
            out["DescendantFonts"].append(
                self["DescendantFonts"][0].__deepcopy__(memodict)
            )
        # DW2
        if "DW2" in self:
            out[Name("DW2")] = List()
            for x in self["DW2"]:
                out["DW2"].append(x)
        # W2
        # CIDToGIDMap
        # default
        for k, v in self.items():
            if k not in out:
                out[k] = copy.deepcopy(v, memodict)
        return out

    def _copy_font_descriptor(self, font_descriptor_to_copy: Dictionary) -> Dictionary:
        f0: Dictionary = font_descriptor_to_copy
        f1: Dictionary = self["FontDescriptor"]
        f1[Name("Type")] = f0.get("Type", Name("FontDescriptor"))
        f1[Name("FontName")] = f0["FontName"]
        if "FontFamily" in f0:
            f1[Name("FontFamily")] = f0["FontFamily"]
        if "FontStretch" in f0:
            f1[Name("FontStretch")] = f0["FontStretch"]
        if "FontWeight" in f0:
            f1[Name("FontWeight")] = f0["FontWeight"]
        f1[Name("Flags")] = f0["Flags"]
        if "FontBBox" in f0 and False:  # TODO
            f1[Name("FontBBox")] = List().set_is_inline(True)
            for i in range(0, len(f0["FontBBox"])):
                f1["FontBBox"].append(f0["FontBBox"][i])
        f1[Name("ItalicAngle")] = f0["ItalicAngle"]
        if "Ascent" in f0:
            f1[Name("Ascent")] = f0["Ascent"]
        if "Descent" in f0:
            f1[Name("Descent")] = f0["Descent"]
        if "Leading" in f0:
            f1[Name("Leading")] = f0["Leading"]
        if "CapHeight" in f0:
            f1[Name("CapHeight")] = f0["CapHeight"]
        if "XHeight" in f0:
            f1[Name("XHeight")] = f0["XHeight"]
        if "StemV" in f0:
            f1[Name("StemV")] = f0["StemV"]
        if "StemH" in f0:
            f1[Name("StemH")] = f0["StemH"]
        if "AvgWidth" in f0:
            f1[Name("AvgWidth")] = f0["AvgWidth"]
        if "MaxWidth" in f0:
            f1[Name("MaxWidth")] = f0["MaxWidth"]
        if "MissingWidth" in f0:
            f1[Name("MissingWidth")] = f0["MissingWidth"]
        if "FontFile" in f0 and False:  # TODO
            f1[Name("FontFile")] = copy.deepcopy(f0["FontFile"])
        if "FontFile2" in f0 and False:  # TODO
            f1[Name("FontFile2")] = copy.deepcopy(f0["FontFile2"])
        if "FontFile3" in f0 and False:  # TODO
            f1[Name("FontFile3")] = copy.deepcopy(f0["FontFile3"])
        if "CharSet" in f0 and False:  # TODO
            f1[Name("CharSet")] = f0["CharSet"]
        # default
        for k, v in f0.items():
            if k not in f1:
                f1[k] = copy.deepcopy(v)
        return f1

    def _empty_copy(self) -> "Font":
        assert False

    # fmt: off
    @staticmethod
    def _read_cmap(cmap_bytes: bytes) -> typing.Dict[int, str]:

        out_map: typing.Dict[int, str] = {}
        cmap_tokenizer: HighLevelTokenizer = HighLevelTokenizer(io.BytesIO(cmap_bytes))

        # process stream
        prev_token: typing.Optional[Token] = None
        number_of_bytes = len(cmap_bytes)
        while cmap_tokenizer.tell() < number_of_bytes:
            token: typing.Optional[Token] = cmap_tokenizer.next_non_comment_token()
            assert token is not None

            # beginbfchar
            if token.get_text() == "beginbfchar":
                assert prev_token is not None
                number_of_lines_001: int = int(prev_token.get_text())
                for _ in range(0, number_of_lines_001):
                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None
                    char_code: int = int(token.get_text()[1:-1], 16)

                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None
                    if token.get_text().startswith("<") and token.get_text().endswith(">"):
                        unicode_str: str = str(token.get_text())[1:-1].replace(" ","")
                        unicode_str = "".join([chr(int(unicode_str[j: j + 4], 16)) for j in range(0, len(unicode_str), 4)])
                    elif token.get_text().startswith("/"):
                        # TODO
                        assert False, "Unsupported CMAP syntax"
                    else:
                        assert False, "Invalid CMAP"
                    out_map[char_code] = unicode_str

            if token.get_text() == "begincidrange":
                assert prev_token is not None
                number_of_lines_002: int = int(prev_token.get_text())
                for _ in range(0, number_of_lines_002):

                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None
                    char_code_start_002: int = int(token.get_text()[1:-1], 16)

                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None
                    char_code_stop_002: int = int(token.get_text()[1:-1], 16)

                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None

                    # <FFFF> <FFFF> 0000
                    if token.get_token_type() == TokenType.NUMBER:
                        unicode_base: int = int(token.get_text())
                        for i in range(char_code_start_002, char_code_stop_002 + 1):
                            out_map[i] = chr(unicode_base + (i - char_code_start_002))

            # beginbfrange
            if token.get_text() == "beginbfrange":
                assert prev_token is not None
                number_of_lines_003: int = int(prev_token.get_text())
                for _ in range(0, number_of_lines_003):

                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None
                    char_code_start_003: int = int(token.get_text()[1:-1], 16)

                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None
                    char_code_stop_003: int = int(token.get_text()[1:-1], 16)

                    token = cmap_tokenizer.next_non_comment_token()
                    assert token is not None

                    # <FFFF> <FFFF> <FFFF>
                    if token.get_token_type() == TokenType.HEX_STRING:
                        unicode_base_str: str = str(token.get_text())[1:-1]
                        for i in range(char_code_start_003, char_code_stop_003 + 1):
                            unicode_hex: str = hex(int(unicode_base_str, 16) + (i - char_code_start_003))[2:]
                            unicode_hex = ("".join(["0" for _ in range(0, 4 - len(unicode_hex) % 4)]) + unicode_hex)
                            unicode_hex = "".join([chr(int(unicode_hex[j: j + 4], 16)) for j in range(0, len(unicode_hex), 4)])
                            out_map[i] = unicode_hex
                        continue

                    # <FFFF> <FFFF> [ <FFFF>* ]
                    if token.get_token_type() == TokenType.START_ARRAY:
                        for i in range(char_code_start_003, char_code_stop_003 + 1):
                            token = cmap_tokenizer.next_non_comment_token()
                            assert token is not None
                            unicode_base_str_003: str = str(token.get_text())[1:-1]
                            unicode_hex = ("".join(["0" for _ in range(0, 4 - len(unicode_base_str_003) % 4)]) + unicode_base_str_003)
                            unicode_hex = "".join([chr(int(unicode_hex[j: j + 4], 16)) for j in range(0, len(unicode_hex), 4)])
                            out_map[i] = unicode_hex
                        # read END_ARRAY
                        token = cmap_tokenizer.next_non_comment_token()
                        assert token is not None
                        assert token.get_token_type() == TokenType.END_ARRAY
                        continue

            # set previous token
            prev_token = token

        # return
        return out_map
    # fmt: on

    #
    # PUBLIC
    #

    def character_identifier_to_unicode(
        self, character_identifier: int
    ) -> typing.Optional[str]:
        """
        This function maps a character identifier to its unicode str.
        If no such mapping exists, this function returns None.
        :param character_identifier:    the character identifier
        :return:                        the matching unicode str
        """
        return None

    def get_ascent(self) -> bDecimal:
        """
        This function returns the maximum height above the baseline reached by glyphs in this font.
        The height of glyphs for accented characters shall be excluded.
        :return:    the ascent
        """
        return bDecimal(0)

    def get_descent(self) -> bDecimal:
        """
        This function returns the maximum depth below the baseline reached by glyphs in this font.
        The value shall be a negative number.
        :return:    the descent
        """
        return bDecimal(0)

    def get_font_name(self) -> typing.Optional[str]:
        """
        This function returns the name of the Font
        e.g. "Helvetica"
        :return:    the name of this Font
        """
        if "BaseFont" in self:
            return str(self["BaseFont"])
        if "FontFamily" in self:
            return str(self["FontFamily"])
        return None

    def get_space_character_width_estimate(self) -> Decimal:
        """
        This function estimates the width of the space character (unicode 32) in this Font.
        If the Font contains the character, this Font will return the corresponding width.

        If the Font does not contain the character, its width may be derived from the
        MissingWidth entry in the FontDescriptor, or the AvgWidth entry.

        If the Font is a composite Font, the DW entry of its DescendantFont is used.

        If all previously mentioned approaches fail, the width is estimated based on characters
        that may be present in the Font. (e.g. the width of 'A' is typically twice that of ' ').
        :return:    (an estimate of) the width of the space character
        """

        # 1. if space is defined, and the width of space is defined, return that
        character_identifier: typing.Optional[
            int
        ] = self.unicode_to_character_identifier(" ")
        width: typing.Optional[Decimal] = None
        if character_identifier is not None:
            width = self.get_width(character_identifier)
            if width is not None:
                return width
        # 2. MissingWidth
        if "FontDescriptor" in self and "MissingWidth" in self["FontDescriptor"]:
            return self["FontDescriptor"]["MissingWidth"] / Decimal(2)
        # 3. AvgWidth
        if "FontDescriptor" in self and "AvgWidth" in self["FontDescriptor"]:
            return self["FontDescriptor"]["AvgWidth"] / Decimal(2)
        # 3. default width
        if (
            "DescendantFonts" in self
            and isinstance(self["DescendantFonts"], List)
            and len(self["DescendantFonts"]) == 1
            and "DW" in self["DescendantFonts"][0]
        ):
            return self["DescendantFonts"][0]["DW"] / Decimal(2)
        # 4. other characters may be defined, which give us a clue
        # fmt: off
        char_to_space_width_ratio: typing.Dict[str, Decimal] = {
            "a": Decimal("0.500"), "b": Decimal("0.500"), "c": Decimal("0.556"),
            "d": Decimal("0.500"), "e": Decimal("0.500"), "f": Decimal("1.000"),
            "g": Decimal("0.500"), "h": Decimal("0.500"), "i": Decimal("1.252"),
            "j": Decimal("1.252"), "k": Decimal("0.556"), "l": Decimal("1.252"),
            "m": Decimal("0.334"), "n": Decimal("0.500"), "o": Decimal("0.500"),
            "p": Decimal("0.500"), "q": Decimal("0.500"), "r": Decimal("0.835"),
            "s": Decimal("0.556"), "t": Decimal("1.000"), "u": Decimal("0.500"),
            "v": Decimal("0.556"), "w": Decimal("0.385"), "x": Decimal("0.556"),
            "y": Decimal("0.556"), "z": Decimal("0.556"), "0": Decimal("0.500"),
            "1": Decimal("0.500"), "2": Decimal("0.500"), "3": Decimal("0.500"),
            "4": Decimal("0.500"), "5": Decimal("0.500"), "6": Decimal("0.500"),
            "7": Decimal("0.500"), "8": Decimal("0.500"), "9": Decimal("0.500"),
            "A": Decimal("0.417"), "B": Decimal("0.417"), "C": Decimal("0.385"),
            "D": Decimal("0.385"), "E": Decimal("0.417"), "F": Decimal("0.455"),
            "G": Decimal("0.357"), "H": Decimal("0.385"), "I": Decimal("1.000"),
            "J": Decimal("0.556"), "K": Decimal("0.417"), "L": Decimal("0.500"),
            "M": Decimal("0.334"), "N": Decimal("0.385"), "O": Decimal("0.357"),
            "P": Decimal("0.417"), "Q": Decimal("0.357"), "R": Decimal("0.385"),
            "S": Decimal("0.417"), "T": Decimal("0.455"), "U": Decimal("0.385"),
            "V": Decimal("0.417"), "W": Decimal("0.294"), "X": Decimal("0.417"),
            "Y": Decimal("0.417"), "Z": Decimal("0.455"),
        }
        # fmt: on
        for k, v in char_to_space_width_ratio.items():
            character_identifier = self.unicode_to_character_identifier(k)
            if character_identifier is not None:
                width = self.get_width(character_identifier)
                if width is not None:
                    return bDecimal(width * v)
        # 5. helvetica
        return Decimal(278)

    def get_width(self, character_identifier: int) -> typing.Optional[bDecimal]:
        """
        This function returns the width (in text space) of a given character identifier.
        If this Font is unable to represent the glyph that corresponds to the character identifier,
        this function returns None
        :param character_identifier:    the character_identifier
        :return:                        the width (in text space) of the character identifier
        """
        return None

    def unicode_to_character_identifier(self, unicode: str) -> typing.Optional[int]:
        """
        This function maps a unicode str to its character identifier.
        If no such mapping exists, this function returns None.
        :param unicode:             the unicode character
        :return:                    the character identifier matching the unicode character
        """
        return None
