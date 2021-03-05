import logging
from decimal import Decimal
from typing import Optional

from ptext.io.read.types import Dictionary, HexadecimalString, Name
from ptext.pdf.canvas.font.cmap.cmap import CMap
from ptext.pdf.canvas.font.glyph_line import GlyphLine, Glyph
from ptext.pdf.canvas.font.latin_text_encoding import (
    StandardEncoding,
    get_encoding,
    WingDings,
)
from ptext.pdf.canvas.geometry.matrix import Matrix

logger = logging.getLogger(__name__)


class Font(Dictionary):
    """
    A font shall be represented in PDF as a dictionary specifying the type of font, its PostScript name, its encoding,
    and information that can be used to provide a substitute when the font program is not available. Optionally, the
    font program may be embedded as a stream object in the PDF file.

    The font types are distinguished by the Subtype entry in the font dictionary. Table 110 lists the font types
    defined in PDF. Type 0 fonts are called composite fonts; other types of fonts are called simple fonts. In addition
    to fonts, PDF supports two classes of font-related objects, called CIDFonts and CMaps, described in 9.7.2,
    "CID-Keyed Fonts Overview". CIDFonts are listed in Table 110 because, like fonts, they are collections of
    glyphs; however, a CIDFont shall not be used directly but only as a component of a Type 0 font.
    """

    def __init__(self):
        super(Font, self).__init__()
        self._font_encoding = None
        self._to_unicode_map = None

    def get_average_character_width(self) -> Optional[Decimal]:
        """
        (Optional) The average width of glyphs in the font. Default value: 0.
        """
        return Decimal(0)

    def get_ascent(self) -> Optional[Decimal]:
        """
        (Required, except for Type 3 fonts) The maximum height above the
        baseline reached by glyphs in this font. The height of glyphs for
        accented characters shall be excluded.
        """
        return Decimal(0)

    def get_descent(self) -> Optional[Decimal]:
        """
        (Required, except for Type 3 fonts) The maximum depth below the
        baseline reached by glyphs in this font. The value shall be a negative
        number.
        """
        return Decimal(0)

    def get_font_matrix(self) -> Matrix:
        return Matrix.identity_matrix()

    def get_font_name(self) -> Optional[str]:
        """
        (Required) The PostScript name of the font. For Type 1 fonts, this is
        always the value of the FontName entry in the font program; for more
        information, see Section 5.2 of the PostScript Language Reference,
        Third Edition. The PostScript name of the font may be used to find the
        font program in the conforming reader or its environment. It is also the
        name that is used when printing to a PostScript output device.
        """
        return None

    def get_missing_character_width(self) -> Decimal:
        """
        (Optional) The width to use for character codes whose widths are not
        specified in a font dictionary’s Widths array. This shall have a
        predictable effect only if all such codes map to glyphs whose actual
        widths are the same as the value of the MissingWidth entry. Default
        value: 0.
        """
        return Decimal(0)

    def get_single_character_width(self, character_code: int) -> Optional[Decimal]:
        """
        Get the width (in text space) of a given character code.
        Returns None if the character code can not be represented in this Font.
        """
        return Decimal(0)

    def get_space_character_width_estimate(self):
        """
        Get the width (in text space) of the space-character.
        If the space character can not be represented using this Font,
        various estimates are attempted (such as missing character width,
        average width, monospaced estimate (if applicable), as well as
        estimates based on the metrics of other characters)
        Returns None if the space character width could not be estimated.
        """
        # TODO
        space_width = self.get_single_character_width(32)

        # missing character width
        if space_width is None:
            logger.debug(
                "Character width for character code 32 was not found. Attempting missing character width."
            )
            space_width = self.get_missing_character_width()

        # average character width
        if space_width is None:
            logger.debug(
                "Missing character width was not found. Attempting average character width."
            )
            space_width = self.get_average_character_width()

        # if [A, B, C, a, b, c] are all the same width, assume the font is monospaced
        if space_width is None:
            logger.debug(
                "Average character width not found. Attempting to check whether font is monospaced."
            )
            character_widths = [
                self.get_single_character_width(self.unicode_to_code(ord(x)))
                for x in "ABCabc"
                if self.can_encode_unicode(ord(x))
                and self.get_single_character_width(self.unicode_to_code(ord(x)))
                is not None
            ]
            if len(character_widths) > 1 and max(character_widths) == min(
                character_widths
            ):
                space_width = character_widths[0]

        # estimate
        if space_width is None:
            logger.debug(
                "Font is not monospaced. Attempting to derive space width from other character widths [a-j]."
            )
            known_characters = [
                ("a", 2),
                ("b", 2),
                ("c", 1.80),
                ("d", 2),
                ("e", 2),
                ("f", 1),
                ("g", 2),
                ("h", 2),
                ("i", 0.80),
                ("j", 0.80),
            ]
            character_widths = [
                self.get_single_character_width(self.unicode_to_code(ord(x)))
                / Decimal(y)
                for x, y in known_characters
                if self.can_encode_unicode(ord(x))
                and self.get_single_character_width(self.unicode_to_code(ord(x)))
                is not None
            ]
            if len(character_widths) > 0:
                space_width = Decimal(sum(character_widths) / len(character_widths))

        # default
        if space_width is None:
            logger.debug(
                "Unable to derive space width from other character widths [a-j]. Returning default."
            )
            space_width = Decimal(250)

        return space_width

    def build_glyph_line(self, content) -> GlyphLine:
        if self._font_encoding is None:
            self._init_font_encoding()
        if self._to_unicode_map is None:
            self._init_to_unicode_map()
        glyphs = []
        i = 0
        value_bytes = content.get_value_bytes()
        while i < len(value_bytes):
            # attempt to use ToUnicode CMAP (2 bytes)
            if i + 1 < len(value_bytes) and isinstance(content, HexadecimalString):
                code = value_bytes[i] * 256 + value_bytes[i + 1]
                if (
                    self._to_unicode_map is not None
                    and self._to_unicode_map.code_to_unicode(code) is not None
                    and self._to_unicode_map.code_to_unicode(code) != 0
                ):
                    unicode = self._to_unicode_map.code_to_unicode(code)
                    glyphs.append(
                        Glyph(code, unicode, self.get_single_character_width(code))
                    )
                    i += 2
                    continue
            # attempt to use ToUnicode CMAP (1 byte)
            code = value_bytes[i]
            if (
                isinstance(content, HexadecimalString)
                and self._to_unicode_map is not None
                and self._to_unicode_map.code_to_unicode(code) is not None
                and self._to_unicode_map.code_to_unicode(code) != 0
            ):
                unicode = self._to_unicode_map.code_to_unicode(code)
                glyphs.append(
                    Glyph(code, unicode, self.get_single_character_width(code))
                )
                i += 1
                continue
            # attempt to use encoding
            if (
                self._font_encoding is not None
                and self._font_encoding.can_encode_character_code(code)
            ):
                unicode = self._font_encoding.code_to_unicode(code)
                glyphs.append(
                    Glyph(code, unicode, self.get_single_character_width(code))
                )
                i += 1
                continue
            # default I guess ?
            i += 1
        # return
        return GlyphLine(glyphs)

    def can_encode_unicode(self, unicode_code: int) -> bool:
        if self._to_unicode_map is not None:
            return self._to_unicode_map.unicode_to_code(unicode_code) != None
        if self._font_encoding is not None:
            return self._font_encoding.can_encode_unicode(unicode_code)
        return False

    def unicode_to_code(self, unicode: int) -> Optional[int]:
        if self._to_unicode_map is not None:
            return self._to_unicode_map.unicode_to_code(unicode)
        if self._font_encoding is not None:
            return self._font_encoding.unicode_to_code(unicode)
        return None

    def _init_font_encoding(self):

        # handle wingdings
        if (
            "FontDescriptor" in self
            and "FontFamily" in self["FontDescriptor"]
            and self["FontDescriptor"]["FontFamily"] == "Wingdings"
        ):
            self._font_encoding = WingDings()
            return

        # no encoding specified
        if "Encoding" not in self:
            self._font_encoding = StandardEncoding()
            return

        # encoding is specified
        if "Encoding" in self and isinstance(self["Encoding"], Name):
            if str(self["Encoding"]).upper() in ["IDENTITY-H", "IDENTITY-V"]:
                self._to_unicode_map = None
            else:
                self._font_encoding = get_encoding(self["Encoding"])
                return

        # differences
        if (
            "Encoding" in self
            and isinstance(self["Encoding"], dict)
            and "Differences" in self["Encoding"]
        ):
            if "BaseEncoding" in self["Encoding"]:
                self._font_encoding = get_encoding(self["Encoding"]["BaseEncoding"])
            else:
                self._font_encoding = StandardEncoding()
            i = 0
            # LEONND font in document 0263_page_0 is not being handled properly
            while i < len(self["Encoding"]["Differences"]):
                start_code = self["Encoding"]["Differences"][i]
                j = 0
                while (i + j + 1) < len(self["Encoding"]["Differences"]) and isinstance(
                    self["Encoding"]["Differences"][i + j + 1], str
                ):
                    c = start_code + j
                    uc = self["Encoding"]["Differences"][i + j + 1]
                    self._font_encoding.add_symbol(c, uc)
                    j += 1
                i += j
                i += 1

        # trim range [FirstChar:]
        if "FirstChar" in self:
            fc = self["FirstChar"]
            self._font_encoding._code_to_unicode = {
                k: v for k, v in self._font_encoding._code_to_unicode.items() if k >= fc
            }
            self._font_encoding._unicode_to_code = {
                k: v for k, v in self._font_encoding._unicode_to_code.items() if v >= fc
            }

        # trim range [:LastChar]
        if "LastChar" in self:
            lc = self["LastChar"]
            self._font_encoding._code_to_unicode = {
                k: v for k, v in self._font_encoding._code_to_unicode.items() if k <= lc
            }
            self._font_encoding._unicode_to_code = {
                k: v for k, v in self._font_encoding._unicode_to_code.items() if v <= lc
            }

    def _init_to_unicode_map(self):
        if "ToUnicode" not in self:
            return
        self._to_unicode_map = CMap().read(
            self["ToUnicode"]["DecodedBytes"].decode("latin1")
        )
