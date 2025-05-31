#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a TrueType font and its properties in a PDF document.

The `TrueTypeFont` class encapsulates the characteristics of a TrueType font, a
popular font format used in PDF documents. TrueType fonts are known for their
scalability and precise control over font rendering, making them ideal for high-quality
text display. This class provides access to font-specific properties, such as glyph
mappings, font metrics, and rendering capabilities, allowing for accurate text layout
and display in PDF documents. As a subclass of `Font`, it extends the basic functionality
of a font while offering specialized handling for TrueType fonts.
"""
import pathlib
import typing

from borb.pdf import CompositeFont
from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.composite_font.cid_type_0_font import CIDType0Font
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.simple_font import SimpleFont
from borb.pdf.primitives import name, stream, PDFType


class TrueTypeFont(SimpleFont):
    """
    Represents a TrueType font and its properties in a PDF document.

    The `TrueTypeFont` class encapsulates the characteristics of a TrueType font, a
    popular font format used in PDF documents. TrueType fonts are known for their
    scalability and precise control over font rendering, making them ideal for high-quality
    text display. This class provides access to font-specific properties, such as glyph
    mappings, font metrics, and rendering capabilities, allowing for accurate text layout
    and display in PDF documents. As a subclass of `Font`, it extends the basic functionality
    of a font while offering specialized handling for TrueType fonts.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __get_cmap_for_type_0_font(
        ttf_font_file: "fontTools.ttLib.ttFont.TTFont",  # type: ignore[name-defined]
    ) -> stream:
        # fmt: off
        cmap_prefix: str = ""
        cmap_prefix += "/CIDInit /ProcSet findresource begin\n"
        cmap_prefix += "12 dict begin\n"
        cmap_prefix += "begincmap\n"
        cmap_prefix += "/CIDSystemInfo <</Registry (Adobe) /Ordering (UCS) /Supplement 0>> def\n"
        cmap_prefix += "/CMapName /Adobe-Identity-UCS def\n"
        cmap_prefix += "/CMapType 2 def\n"
        cmap_prefix += "1 begincodespacerange\n"
        cmap_prefix += "<0000> <FFFF>\n"
        cmap_prefix += "endcodespacerange\n"
        # fmt: on

        # 1 beginbfchar
        # <0000> <0000>
        # endbfchar
        import fontTools.agl  # type: ignore[import-not-found]

        pairs: typing.List[typing.Tuple[str, str]] = []
        for character_code, character_name in enumerate(ttf_font_file.glyphOrder):
            g_unicode = fontTools.agl.toUnicode(character_name)
            if len(g_unicode) == 0:
                continue
            g_hex: str = ""
            if len(g_unicode) == 1:
                g_hex = hex(ord(g_unicode))[2:]
            if len(g_unicode) == 2:
                g_hex = hex(ord(g_unicode[0]))[2:] + hex(ord(g_unicode[1]))[2:]
            while len(g_hex) < 4:
                g_hex = "0" + g_hex
            i_hex: str = hex(character_code)[2:]
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

        # convert to stream object
        import zlib

        bts: bytes = (cmap_prefix + cmap_content + cmap_suffix).encode("latin1")
        to_unicode_stream = stream()
        to_unicode_stream[name("Bytes")] = zlib.compress(bts, 9)
        to_unicode_stream[name("DecodedBytes")] = bts
        to_unicode_stream[name("Filter")] = name("FlateDecode")
        to_unicode_stream[name("Length")] = len(to_unicode_stream[name("Bytes")])

        # return
        from borb.pdf.font.cmap import CMap

        return CMap(to_unicode_stream)

    @staticmethod
    def __get_font_descriptor(ttf_font_file: "fontTools.ttLib.ttFont.TTFont") -> dict:  # type: ignore[name-defined]

        # determine FontBBox, CapHeight
        try:
            from fontTools.pens.boundsPen import BoundsPen  # type: ignore[import-not-found, import-untyped]
        except ImportError:
            raise ImportError(
                "Please install the 'fontTools' library to use the TrueTypeFont class. "
                "You can install it with 'pip install fonttools'."
            )
        units_per_em: float = ttf_font_file["head"].unitsPerEm
        min_x: float = 1000
        min_y: float = 1000
        max_x: float = 0
        max_y: float = 0
        cap_height: typing.Optional[float] = None
        glyph_set = ttf_font_file.getGlyphSet()
        for glyph_name in ttf_font_file.glyphOrder:

            # (attempt to) determine bounds of glyph
            pen = BoundsPen(glyph_set)
            glyph_set[glyph_name].draw(pen)
            if pen.bounds is None:
                continue

            # IF the glyph is a large uppercase letter
            # THEN update cap_height
            if glyph_name in "EFHIJLMNTZ" and cap_height is None:
                cap_height = pen.bounds[3]

            # update min_x, min_y, max_x, max_y
            min_x = min(min_x, pen.bounds[0] / units_per_em * 1000)
            min_y = min(min_y, pen.bounds[1] / units_per_em * 1000)
            max_x = max(max_x, pen.bounds[2] / units_per_em * 1000)
            max_y = max(max_y, pen.bounds[3] / units_per_em * 1000)

        # IF cap_height is not set
        # THEN use a sensible default
        cap_height = cap_height or 840

        # build font_descriptor
        font_descriptor: typing.Dict[name, PDFType] = {
            name("Ascent"): ttf_font_file["hhea"].ascent / units_per_em * 1000,
            name("CapHeight"): cap_height,
            name("Descent"): ttf_font_file["hhea"].descent / units_per_em * 1000,
            name("Flags"): 4,
            name("FontBBox"): [min_x, min_y, max_x, max_y],
            name("FontName"): TrueTypeFont.__get_font_name(ttf_font_file),
            name("FontStretch"): name("Normal"),
            name("FontWeight"): 400,
            name("ItalicAngle"): ttf_font_file["post"].italicAngle,
            name("StemV"): 297,
            name("Type"): name("FontDescriptor"),
        }

        # return
        return font_descriptor

    @staticmethod
    def __get_font_file_stream(font_file_bytes: bytes) -> stream:
        import zlib

        font_file_stream: stream = stream()
        font_file_stream[name("Bytes")] = zlib.compress(font_file_bytes, 9)
        font_file_stream[name("Filter")] = name("FlateDecode")
        font_file_stream[name("Length")] = len(font_file_stream[name("Bytes")])
        font_file_stream[name("Length1")] = len(font_file_bytes)
        font_file_stream[name("Type")] = name("Font")
        return font_file_stream

    @staticmethod
    def __get_font_name(ttf_font_file: "fontTools.ttLib.ttFont.TTFont") -> str:  # type: ignore[name-defined]

        # derive the font_name
        font_name: str = next(
            iter(
                [
                    x.string
                    for x in ttf_font_file["name"].names
                    if x.platformID == 3 and x.platEncID == 1 and x.nameID == 6
                ]
            ),
            b"",
        ).decode("latin1")

        # IF the font_name consists of pairs of <\x00><char>
        # THEN we leave out every even character
        if all([font_name[i] == "\x00" for i in range(0, len(font_name), 2)]):
            font_name = "".join([font_name[i] for i in range(1, len(font_name), 2)])

        # return
        return font_name

    @staticmethod
    def __true_type_from_file(where_from: pathlib.Path) -> "Font":

        # get the bytes
        font_file_bytes: bytes = b""
        with open(where_from, "rb") as font_file_handle:
            font_file_bytes = font_file_handle.read()

        # determine character_code_to_character_name
        # AND its inverse
        # fmt: off
        import io
        try:
            from fontTools.ttLib import TTFont  # type: ignore[import-not-found, import-untyped]
        except ImportError:
            raise ImportError(
                "Please install the 'fontTools' library to use the TrueTypeFont class. "
                "You can install it with 'pip install fonttools'."
            )
        ttf_font_file: TTFont = TTFont(io.BytesIO(font_file_bytes))
        character_code_to_character_name: typing.Dict[int, str] = ttf_font_file.getBestCmap()
        character_name_to_character_code: typing.Dict[str, int] =  {v:k for k,v in character_code_to_character_name.items()}
        # fmt: on

        # limit the character_code_to_character_name to those that appear in AdobeGlyphList
        # fmt: off
        character_code_to_character_name = {k:v for k,v in character_code_to_character_name.items() if v in AdobeGlyphList.ADOBE_CHARACTER_NAME_TO_CHARACTER.keys()}
        character_name_to_character_code = {k:v for k,v in character_name_to_character_code.items() if k in AdobeGlyphList.ADOBE_CHARACTER_NAME_TO_CHARACTER.keys()}
        # fmt: on

        # glyphs in order
        glyphs_in_order: typing.List[str] = [
            y[0]
            for y in sorted(
                [(k, v) for k, v in character_name_to_character_code.items()],
                key=lambda x: x[1],
            )
        ]

        # IF the highest character_code is higher than 255
        # THEN we need something other than a TrueTypeFont
        if max(character_code_to_character_name.keys()) >= 256:
            type_0_font: Font = TrueTypeFont.__type_0_font_from_file(
                where_from=where_from
            )
            type_0_font[name("DescendantFonts")][0][name("FontDescriptor")][
                name("FontFile2")
            ] = TrueTypeFont.__get_font_file_stream(font_file_bytes)
            return type_0_font

        # fill in TrueTypeFont
        # fmt: off
        true_type_font: TrueTypeFont = TrueTypeFont()
        true_type_font[name("BaseFont")] = name(TrueTypeFont.__get_font_name(ttf_font_file))
        true_type_font[name('Encoding')] = {}
        true_type_font[name('Encoding')][name('BaseEncoding')] = name('WinAnsiEncoding')
        true_type_font[name('Encoding')][name('Differences')] = [character_name_to_character_code[glyphs_in_order[i//2]] if i % 2 == 0 else glyphs_in_order[i//2] for i in range(0, len(glyphs_in_order)*2)]
        true_type_font[name('FontDescriptor')] = TrueTypeFont.__get_font_descriptor(ttf_font_file=ttf_font_file)
        true_type_font[name('FontDescriptor')][name('FontFile2')] = TrueTypeFont.__get_font_file_stream(font_file_bytes=font_file_bytes)
        true_type_font[name("FirstChar")] = min(character_code_to_character_name.keys())
        true_type_font[name("LastChar")] = max(character_code_to_character_name.keys())
        true_type_font[name("Name")] = true_type_font[name("BaseFont")]
        true_type_font[name("Widths")] = [ttf_font_file.getGlyphSet()[k].width for k in character_name_to_character_code.keys()]
        # fmt: on

        # return
        return true_type_font

    @staticmethod
    def __type_0_font_from_file(where_from: pathlib.Path) -> "Font":

        # get the bytes
        font_file_bytes: bytes = b""
        with open(where_from, "rb") as font_file_handle:
            font_file_bytes = font_file_handle.read()

        # determine character_code_to_character_name
        # AND its inverse
        # fmt: off
        import io
        try:
            from fontTools.ttLib import TTFont  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'fontTools' library to use the TrueTypeFont class. "
                "You can install it with 'pip install fonttools'."
            )
        ttf_font_file: TTFont = TTFont(io.BytesIO(font_file_bytes))
        character_code_to_character_name: typing.Dict[int, str] = ttf_font_file.getBestCmap()
        character_name_to_character_code: typing.Dict[str, int] =  {v:k for k,v in character_code_to_character_name.items()}
        # fmt: on

        # limit the character_code_to_character_name to those that appear in AdobeGlyphList
        # fmt: off
        character_code_to_character_name = {k:v for k,v in character_code_to_character_name.items() if v in AdobeGlyphList.ADOBE_CHARACTER_NAME_TO_CHARACTER.keys()}
        character_name_to_character_code = {k:v for k,v in character_name_to_character_code.items() if k in AdobeGlyphList.ADOBE_CHARACTER_NAME_TO_CHARACTER.keys()}
        # fmt: on

        # build /W
        units_per_em: float = ttf_font_file["head"].unitsPerEm
        ttf_font_file_glyphs = ttf_font_file.getGlyphSet()
        ttf_font_file_cmap = ttf_font_file.getBestCmap()
        widths_array: typing.List[typing.Any] = []
        for character_id, glyph_name in enumerate(ttf_font_file.glyphOrder):
            widths_array += [character_id]
            try:
                glyph_str: str = AdobeGlyphList.ADOBE_CHARACTER_NAME_TO_CHARACTER[
                    glyph_name
                ]
                glyph_unicode: int = ord(glyph_str)
                widths_array += [
                    [
                        round(
                            ttf_font_file_glyphs[
                                ttf_font_file_cmap[glyph_unicode]
                            ].width
                            / units_per_em
                            * 1000,
                            2,
                        )
                    ]
                ]
            except:
                widths_array += [[0]]

        # build Type0Font
        # fmt: off
        type_0_font: Font = CompositeFont()
        type_0_font[name("BaseFont")] = name(TrueTypeFont.__get_font_name(ttf_font_file))
        type_0_font[name("DescendantFonts")] = []
        type_0_font[name("DescendantFonts")] += [CIDType0Font()]
        type_0_font[name("DescendantFonts")][0][name("Type")] = name("Font")
        type_0_font[name("DescendantFonts")][0][name("Subtype")] = name("CIDFontType2")
        type_0_font[name("DescendantFonts")][0][name("BaseFont")] = type_0_font[name("BaseFont")]
        type_0_font[name("DescendantFonts")][0][name("FontDescriptor")] = TrueTypeFont.__get_font_descriptor(ttf_font_file=ttf_font_file)
        type_0_font[name("DescendantFonts")][0][name("DW")] = 250
        type_0_font[name("DescendantFonts")][0][name("W")] =  widths_array
        type_0_font[name("DescendantFonts")][0][name("CIDToGIDMap")] = name("Identity")
        type_0_font[name("DescendantFonts")][0][name("CIDSystemInfo")] = {}
        type_0_font[name("DescendantFonts")][0][name("CIDSystemInfo")][name("Registry")] = "Adobe"
        type_0_font[name("DescendantFonts")][0][name("CIDSystemInfo")][name("Ordering")] = "Identity"
        type_0_font[name("DescendantFonts")][0][name("CIDSystemInfo")][name("Supplement")] = 0
        type_0_font[name("Encoding")] = name("Identity-H")
        type_0_font[name("Subtype")] = name("Type0")
        type_0_font[name("ToUnicode")] = TrueTypeFont.__get_cmap_for_type_0_font(ttf_font_file)
        # fmt: on

        # return
        return type_0_font

    #
    # PUBLIC
    #

    @staticmethod
    def from_file(where_from: typing.Union[str, pathlib.Path]) -> "Font":
        """
        Create a Font instance from a TrueType font file.

        :param where_from:  The file path to the TrueType font file. Can be provided as a string or a `pathlib.Path` object.
        :return:            An instance of the Font class representing the loaded TrueType font.
        """
        # convert str to pathlib.Path
        if isinstance(where_from, str):
            where_from = pathlib.Path(where_from)

        # verify the pathlib.Path exists
        if isinstance(where_from, pathlib.Path):
            assert where_from.exists()
            assert where_from.name.endswith(".ttf")

        # return
        return TrueTypeFont.__true_type_from_file(where_from=where_from)
