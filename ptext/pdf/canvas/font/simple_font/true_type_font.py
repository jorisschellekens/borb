#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The TrueType font format was developed by Apple Computer, Inc., and has been adopted as a standard font
format for the Microsoft Windows operating system. Specifications for the TrueType font file format are
available in Apple’s TrueType Reference Manual and Microsoft’s TrueType 1.0 Font Files Technical
Specification (see Bibliography).
"""
import typing
import zlib
from decimal import Decimal
from pathlib import Path

from fontTools.ttLib import TTFont  # type: ignore [import]

from ptext.io.read.types import Decimal as pDecimal
from ptext.io.read.types import Name, List, Dictionary, String, Stream
from ptext.pdf.canvas.font.simple_font.font_type_1 import Type1Font


class TrueTypeFont(Type1Font):
    """
    A TrueType font dictionary may contain the same entries as a Type 1 font dictionary (see Table 111), with these
    differences:
    •   The value of Subtype shall be TrueType.
    •   The value of Encoding is subject to limitations that are described in 9.6.6, "Character Encoding".
    •   The value of BaseFont is derived differently. The PostScript name for the value of BaseFont may be determined in one of two ways:
    •   If the TrueType font program's “name” table contains a PostScript name, it shall be used.
    •   In the absence of such an entry in the “name” table, a PostScript name shall be derived from the name by
        which the font is known in the host operating system. On a Windows system, the name shall be based on
        the lfFaceName field in a LOGFONT structure; in the Mac OS, it shall be based on the name of the FOND
        resource. If the name contains any SPACEs, the SPACEs shall be removed.
    """

    @staticmethod
    def true_type_font_from_file(path_to_font_file: Path) -> "TrueTypeFont":
        """
        This function returns the PDF TrueTypeFont object for a given TTF file
        """
        assert path_to_font_file.exists()
        assert path_to_font_file.name.endswith(".ttf")

        font_file_bytes: typing.Optional[bytes] = None
        with open(path_to_font_file, "rb") as ffh:
            font_file_bytes = ffh.read()
        assert font_file_bytes

        # read file
        ttf_font_file = TTFont(path_to_font_file)

        # build font
        font: TrueTypeFont = TrueTypeFont()
        font_name: str = str(
            [
                x
                for x in ttf_font_file["name"].names
                if x.platformID == 3 and x.nameID == 1
            ][0].string,
            "latin1",
        )
        font_name = "".join(
            [x for x in font_name if x.lower() in "abcdefghijklmnopqrstuvwxyz"]
        )

        font[Name("Name")] = Name(font_name)
        font[Name("BaseFont")] = Name(font_name)

        cmap: typing.Optional[typing.Dict[int, str]] = ttf_font_file.getBestCmap()
        cmap_reverse: typing.Dict[str, int] = {}
        for k, v in cmap.items():
            if v in cmap_reverse:
                cmap_reverse[v] = min(cmap_reverse[v], k)
            else:
                cmap_reverse[v] = k
        glyph_order: typing.List[str] = [
            x for x in ttf_font_file.glyphOrder if x in cmap_reverse
        ]

        # build widths
        units_per_em: pDecimal = pDecimal(ttf_font_file["head"].unitsPerEm)
        if cmap is not None:
            font[Name("FirstChar")] = pDecimal(0)
            font[Name("LastChar")] = pDecimal(len(glyph_order))
            font[Name("Widths")] = List()
            for glyph_name in glyph_order:
                w: typing.Union[pDecimal, Decimal] = (
                    pDecimal(ttf_font_file.getGlyphSet()[glyph_name].width)
                    / units_per_em
                ) * Decimal(1000)
                w = pDecimal(round(w, 2))
                font["Widths"].append(w)

        font[Name("FontDescriptor")] = Dictionary()
        font["FontDescriptor"][Name("Type")] = Name("FontDescriptor")
        font["FontDescriptor"][Name("FontName")] = String(font_name)
        font["FontDescriptor"][Name("FontStretch")] = Name("Normal")  # TODO
        font["FontDescriptor"][Name("FontWeight")] = pDecimal(400)  # TODO
        font["FontDescriptor"][Name("Flags")] = pDecimal(4)  # TODO
        font["FontDescriptor"][Name("FontBBox")] = List().set_can_be_referenced(  # type: ignore [attr-defined]
            False
        )  # TODO
        for _ in range(0, 4):
            font["FontDescriptor"]["FontBBox"].append(pDecimal(0))

        # fmt: off
        font["FontDescriptor"][Name("ItalicAngle")] = pDecimal(ttf_font_file["post"].italicAngle)
        font["FontDescriptor"][Name("Ascent")] = pDecimal(pDecimal(ttf_font_file["hhea"].ascent) / units_per_em * Decimal(1000))
        font["FontDescriptor"][Name("Descent")] = pDecimal(pDecimal(ttf_font_file["hhea"].descent) / units_per_em * Decimal(1000))
        font["FontDescriptor"][Name("CapHeight")] = pDecimal(0)         # TODO
        font["FontDescriptor"][Name("StemV")] = pDecimal(0)             # TODO
        # fmt: on

        font[Name("Encoding")] = Dictionary()
        font["Encoding"][Name("BaseEncoding")] = Name("WinAnsiEncoding")
        font["Encoding"][Name("Differences")] = List()
        for i in range(0, len(glyph_order)):
            font["Encoding"]["Differences"].append(pDecimal(i))
            font["Encoding"]["Differences"].append(Name(glyph_order[i]))

        # embed font file
        font_stream: Stream = Stream()
        font_stream[Name("Type")] = Name("Font")
        font_stream[Name("Subtype")] = Name("TrueType")
        font_stream[Name("Length")] = pDecimal(len(font_file_bytes))
        font_stream[Name("Length1")] = pDecimal(len(font_file_bytes))
        font_stream[Name("Filter")] = Name("FlateDecode")
        font_stream[Name("DecodedBytes")] = font_file_bytes
        font_stream[Name("Bytes")] = zlib.compress(font_file_bytes, 9)

        font["FontDescriptor"][Name("FontFile2")] = font_stream

        # return
        return font

    def __init__(self):
        super(TrueTypeFont, self).__init__()
        self[Name("Subtype")] = Name("TrueType")

    def _empty_copy(self) -> "Font":  # type: ignore [name-defined]
        return TrueTypeFont()

    def __deepcopy__(self, memodict={}):
        # fmt: off
        f_out: TrueTypeFont = super(TrueTypeFont, self).__deepcopy__(memodict)
        f_out[Name("Subtype")] = Name("TrueType")
        f_out._character_identifier_to_unicode_lookup: typing.Dict[int, str] = {k: v for k, v in self._character_identifier_to_unicode_lookup.items()}
        f_out._unicode_lookup_to_character_identifier: typing.Dict[str, int] = {k: v for k, v in self._unicode_lookup_to_character_identifier.items()}
        return f_out
        # fmt: on
