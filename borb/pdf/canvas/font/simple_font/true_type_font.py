#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The TrueType font format was developed by Apple Computer, Inc., and has been adopted as a standard font
format for the Microsoft Windows operating system. Specifications for the TrueType font file format are
available in Apple’s TrueType Reference Manual and Microsoft’s TrueType 1.0 Font Files Technical
Specification (see Bibliography).
"""
import io
import typing
import zlib
from decimal import Decimal
import pathlib

from fontTools.agl import toUnicode  # type: ignore[import]
from fontTools.pens.boundsPen import BoundsPen  # type: ignore[import]
from fontTools.ttLib import TTFont  # type: ignore[import]

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import Stream
from borb.io.read.types import String
from borb.pdf.canvas.font.composite_font.cid_font_type_2 import CIDType2Font
from borb.pdf.canvas.font.composite_font.font_type_0 import Type0Font
from borb.pdf.canvas.font.simple_font.font_type_1 import Type1Font


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

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(TrueTypeFont, self).__init__()
        self[Name("Subtype")] = Name("TrueType")

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        # fmt: off
        f_out: TrueTypeFont = super(TrueTypeFont, self).__deepcopy__(memodict)
        f_out[Name("Subtype")] = Name("TrueType")
        f_out._character_identifier_to_unicode_lookup: typing.Dict[int, str] = {k: v for k, v in self._character_identifier_to_unicode_lookup.items()}
        f_out._unicode_lookup_to_character_identifier: typing.Dict[str, int] = {k: v for k, v in self._unicode_lookup_to_character_identifier.items()}
        return f_out
        # fmt: on

    @staticmethod
    def _build_custom_cmap_for_type_0_font(ttf_font_file: TTFont) -> Stream:
        cmap_prefix: str = """
        /CIDInit /ProcSet findresource begin
        12 dict begin
        begincmap
        /CIDSystemInfo <</Registry (Adobe) /Ordering (UCS) /Supplement 0>> def
        /CMapName /Adobe-Identity-UCS def
        /CMapType 2 def
        1 begincodespacerange
        <0000> <FFFF>
        endcodespacerange
        """
        # 1 beginbfchar
        # <0000> <0000>
        # endbfchar
        pairs: typing.List[typing.Tuple[str, str]] = []
        for cid, g in enumerate(ttf_font_file.glyphOrder):
            g_unicode: str = toUnicode(g)
            if len(g_unicode) == 0:
                continue
            g_hex: str = ""
            if len(g_unicode) == 1:
                g_hex = hex(ord(g_unicode))[2:]
            if len(g_unicode) == 2:
                g_hex = hex(ord(g_unicode[0]))[2:] + hex(ord(g_unicode[1]))[2:]
            while len(g_hex) < 4:
                g_hex = "0" + g_hex
            i_hex: str = hex(cid)[2:]
            while len(i_hex) < 4:
                i_hex = "0" + i_hex
            pairs.append((i_hex, g_hex))

        # split in lots of 100
        cmap_content: str = ""
        for i in range(0, len(pairs), 100):
            start_index: int = i
            end_index: int = min(start_index + 100, len(pairs))
            n: int = end_index - start_index
            cmap_content += "%d beginbfchar\n" % n
            for j in range(start_index, end_index):
                cmap_content += "<%s> <%s>\n" % (pairs[j][0], pairs[j][1])
            cmap_content += "endbfchar\n"

        cmap_suffix: str = (
            "endcmap\nCMapName currentdict /CMap defineresource pop\nend\nend\n"
        )

        bts: bytes = (cmap_prefix + cmap_content + cmap_suffix).encode("latin1")
        to_unicode_stream = Stream()
        to_unicode_stream[Name("DecodedBytes")] = bts
        to_unicode_stream[Name("Bytes")] = zlib.compress(bts, 9)
        to_unicode_stream[Name("Filter")] = Name("FlateDecode")
        to_unicode_stream[Name("Length")] = bDecimal(len(bts))
        return to_unicode_stream

    @staticmethod
    def _build_custom_widths_array_for_type_0_font(ttf_font_file: TTFont) -> List:
        units_per_em: bDecimal = bDecimal(ttf_font_file["head"].unitsPerEm)
        cmap = ttf_font_file.getBestCmap()
        glyph_set = ttf_font_file.getGlyphSet()
        widths_array: List = List()
        for cid, g in enumerate(ttf_font_file.glyphOrder):
            glyph_width: bDecimal = bDecimal(0)
            try:
                glyph_width = bDecimal(
                    glyph_set[cmap[ord(toUnicode(g))]].width / units_per_em * 1000
                )
            except:
                pass
            widths_array.append(bDecimal(cid))
            widths_array.append(List())
            widths_array[-1].append(bDecimal(glyph_width))
        return widths_array

    def _empty_copy(self) -> "Font":  # type: ignore[name-defined]
        return TrueTypeFont()

    @staticmethod
    def _get_base_font(ttf_font_file: TTFont) -> str:
        font_name: str = str(
            [
                x
                for x in ttf_font_file["name"].names
                if x.platformID == 3 and x.platEncID == 1 and x.nameID == 6
            ][0].string,
            "latin1",
        )
        font_name = "".join(
            [x for x in font_name if x.lower() in "abcdefghijklmnopqrstuvwxyz-"]
        )
        return font_name

    @staticmethod
    def _get_font_descriptor(ttf_font_file: TTFont) -> Dictionary:
        # fmt: off
        font_descriptor: Dictionary = Dictionary()
        font_descriptor[Name("Type")] = Name("FontDescriptor")
        font_descriptor[Name("FontName")] = String(TrueTypeFont._get_base_font(ttf_font_file))
        font_descriptor[Name("FontStretch")] = Name("Normal")  # TODO
        font_descriptor[Name("FontWeight")] = bDecimal(400)  # TODO
        font_descriptor[Name("Flags")] = bDecimal(4)  # TODO
        # fmt: on

        # determine FontBBox, CapHeight
        units_per_em: float = ttf_font_file["head"].unitsPerEm
        min_x: float = 1000
        min_y: float = 1000
        max_x: float = 0
        max_y: float = 0
        cap_height: typing.Optional[bDecimal] = None
        glyph_set = ttf_font_file.getGlyphSet()
        for glyph_name in ttf_font_file.glyphOrder:
            pen = BoundsPen(glyph_set)
            glyph_set[glyph_name].draw(pen)
            if pen.bounds is None:
                continue
            # determine CapHeight
            if glyph_name in "EFHIJLMNTZ" and cap_height is None:
                cap_height = bDecimal(pen.bounds[3])
            min_x = min(min_x, pen.bounds[0] / units_per_em * 1000)
            min_y = min(min_y, pen.bounds[1] / units_per_em * 1000)
            max_x = max(max_x, pen.bounds[2] / units_per_em * 1000)
            max_y = max(max_y, pen.bounds[3] / units_per_em * 1000)
        if cap_height is None:
            cap_height = bDecimal(840)

        font_descriptor[Name("FontBBox")] = List().set_is_inline(True)
        font_descriptor["FontBBox"].append(bDecimal(min_x))
        font_descriptor["FontBBox"].append(bDecimal(min_y))
        font_descriptor["FontBBox"].append(bDecimal(max_x))
        font_descriptor["FontBBox"].append(bDecimal(max_y))

        # fmt: off
        font_descriptor[Name("ItalicAngle")] = bDecimal(ttf_font_file["post"].italicAngle)
        font_descriptor[Name("Ascent")] = bDecimal(ttf_font_file["hhea"].ascent / units_per_em * 1000)
        font_descriptor[Name("Descent")] = bDecimal(ttf_font_file["hhea"].descent / units_per_em * 1000)
        font_descriptor[Name("CapHeight")] = cap_height
        font_descriptor[Name("StemV")] = bDecimal(297)             # TODO
        # fmt: on

        return font_descriptor

    @staticmethod
    def _get_font_file_stream(font_file_bytes: bytes) -> Stream:
        font_stream: Stream = Stream()
        font_stream[Name("Type")] = Name("Font")
        font_stream[Name("Length")] = bDecimal(len(font_file_bytes))
        font_stream[Name("Length1")] = bDecimal(len(font_file_bytes))
        font_stream[Name("Filter")] = Name("FlateDecode")
        font_stream[Name("DecodedBytes")] = font_file_bytes
        font_stream[Name("Bytes")] = zlib.compress(font_file_bytes, 9)
        return font_stream

    @staticmethod
    def _type_0_font_from_file(ttf_font_file: TTFont) -> "Type0Font":
        type_0_font: Type0Font = Type0Font()

        # build BaseFont
        font_name: str = TrueTypeFont._get_base_font(ttf_font_file)
        type_0_font[Name("BaseFont")] = Name(font_name)

        # set Encoding
        type_0_font[Name("Encoding")] = Name("Identity-H")

        # set ToUnicode
        type_0_font[
            Name("ToUnicode")
        ] = TrueTypeFont._build_custom_cmap_for_type_0_font(ttf_font_file)

        # build DescendantFont
        descendant_font: CIDType2Font = CIDType2Font()
        descendant_font[Name("Type")] = Name("Font")
        descendant_font[Name("Subtype")] = Name("CIDFontType2")
        descendant_font[Name("BaseFont")] = Name(font_name)
        descendant_font[Name("FontDescriptor")] = TrueTypeFont._get_font_descriptor(
            ttf_font_file
        )
        descendant_font[Name("DW")] = bDecimal(250)

        # build W array
        descendant_font[
            Name("W")
        ] = TrueTypeFont._build_custom_widths_array_for_type_0_font(ttf_font_file)
        descendant_font[Name("CIDToGIDMap")] = Name("Identity")

        # build CIDSystemInfo
        # fmt: off
        descendant_font[Name("CIDSystemInfo")] = Dictionary()
        descendant_font[Name("CIDSystemInfo")][Name("Registry")] = String("Adobe")
        descendant_font[Name("CIDSystemInfo")][Name("Ordering")] = String("Identity")
        descendant_font[Name("CIDSystemInfo")][Name("Supplement")] = bDecimal(0)
        # fmt: on

        # add to DescendantFonts
        type_0_font[Name("DescendantFonts")] = List()
        type_0_font[Name("DescendantFonts")].append(descendant_font)

        # return
        return type_0_font

    #
    # PUBLIC
    #

    @staticmethod
    def true_type_font_from_file(
        font_file: typing.Union[pathlib.Path, bytes],
    ) -> typing.Union["TrueTypeFont", "Type0Font"]:
        """
        This function returns the PDF TrueTypeFont object for a given TTF file
        :param font_file:   the font file (as a Path, or bytes)
        :return:            a TrueTypeFont or Type0Font
        """
        if isinstance(font_file, pathlib.Path):
            assert font_file.exists()
            assert font_file.name.endswith(".ttf")

        # read bytes if needed
        font_file_bytes: typing.Optional[bytes] = None
        if isinstance(font_file, pathlib.Path):
            with open(font_file, "rb") as ffh:
                font_file_bytes = ffh.read()
            assert font_file_bytes
        else:
            font_file_bytes = font_file

        # read file
        ttf_font_file: TTFont = TTFont(io.BytesIO(font_file_bytes))

        # read cmap
        cmap: typing.Optional[typing.Dict[int, str]] = ttf_font_file.getBestCmap()
        assert cmap is not None
        cmap_reverse: typing.Dict[str, int] = {}
        for k, v in cmap.items():
            if v in cmap_reverse:
                cmap_reverse[v] = min(cmap_reverse[v], k)
            else:
                cmap_reverse[v] = k
        glyph_order: typing.List[str] = [
            x for x in ttf_font_file.glyphOrder if x in cmap_reverse
        ]

        # if there are more than 256 glyphs, we need to switch to a Type0Font
        if len(glyph_order) >= 256:
            # fmt: off
            type_0_font: Type0Font = TrueTypeFont._type_0_font_from_file(ttf_font_file)
            type_0_font["DescendantFonts"][0]["FontDescriptor"][Name("FontFile2")] = TrueTypeFont._get_font_file_stream(font_file_bytes)
            return type_0_font
            # fmt: on

        # build font
        font: TrueTypeFont = TrueTypeFont()
        font_name: str = TrueTypeFont._get_base_font(ttf_font_file)
        font[Name("Name")] = Name(font_name)
        font[Name("BaseFont")] = Name(font_name)

        # build widths
        units_per_em: bDecimal = bDecimal(ttf_font_file["head"].unitsPerEm)
        if cmap is not None:
            # fmt: off
            font[Name("FirstChar")] = bDecimal(min([cid for cid, _ in enumerate(glyph_order)]))
            font[Name("LastChar")] = bDecimal(max([cid for cid, _ in enumerate(glyph_order)]))
            # fmt: on
            font[Name("Widths")] = List()
            for glyph_name in glyph_order:
                w: typing.Union[bDecimal, Decimal] = (
                    bDecimal(ttf_font_file.getGlyphSet()[glyph_name].width)
                    / units_per_em
                ) * Decimal(1000)
                w = bDecimal(round(w, 2))
                font["Widths"].append(w)

        assert font[Name("FirstChar")] >= 0
        assert (
            font[Name("LastChar")] < 256
        ), "TrueType fonts with more than 256 glyphs are currently not supported."

        font[Name("FontDescriptor")] = TrueTypeFont._get_font_descriptor(ttf_font_file)
        font[Name("Encoding")] = Dictionary()
        font["Encoding"][Name("BaseEncoding")] = Name("WinAnsiEncoding")
        font["Encoding"][Name("Differences")] = List()
        for i in range(0, len(glyph_order)):
            font["Encoding"]["Differences"].append(bDecimal(i))
            font["Encoding"]["Differences"].append(Name(glyph_order[i]))

        # embed font file
        # fmt: off
        font["FontDescriptor"][Name("FontFile2")] = TrueTypeFont._get_font_file_stream(font_file_bytes)
        # fmt: on

        # return
        return font
