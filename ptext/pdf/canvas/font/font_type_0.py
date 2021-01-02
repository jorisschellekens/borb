import copy
from decimal import Decimal
from typing import Optional

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.font.glyph_line import GlyphLine


class FontType0(Font):
    """
    A composite font, also called a Type 0 font, is one whose glyphs are obtained from a fontlike object called a
    CIDFont. A composite font shall be represented by a font dictionary whose Subtype value is Type0. The Type
    0 font is known as the root font, and its associated CIDFont is called its descendant.
    """

    def get_average_character_width(self) -> Optional[Decimal]:
        return self.get_descendant_font().get_average_character_width()

    def get_ascent(self) -> Optional[Decimal]:
        return self.get_descendant_font().get_ascent()

    def get_descent(self) -> Optional[Decimal]:
        return self.get_descendant_font().get_descent()

    def get_single_character_width(self, character_code: int) -> Optional[Decimal]:
        return self.get_descendant_font().get_single_character_width(character_code)

    def get_missing_character_width(self) -> Decimal:
        return self.get_descendant_font().get_missing_character_width()

    def get_font_name(self) -> Optional[str]:
        return self.get_descendant_font().get_font_name()

    def get_descendant_font(self) -> Font:
        if "DescendantFonts" not in self:
            raise PDFTypeError(expected_type=list, received_type=None)
        if isinstance(self["DescendantFonts"], list):
            if not isinstance(self["DescendantFonts"][0], Font):
                raise PDFTypeError(
                    expected_type=Font, received_type=self["DescendantFonts"][0]
                )
            return self["DescendantFonts"][0]
        if isinstance(self["DescendantFonts"], Font):
            return self["DescendantFonts"]
        raise PDFTypeError(expected_type=Font, received_type=None)

    def build_glyph_line(self, content) -> GlyphLine:
        if self._font_encoding is None:
            self._init_font_encoding()
        if self._to_unicode_map is None:
            self._init_to_unicode_map()
        # set parent
        self.get_descendant_font()._parent = self  # type: ignore [attr-defined]
        # call child
        return self.get_descendant_font().build_glyph_line(content)

    def __deepcopy__(self, memodict={}):
        copy_out = FontType0()
        copy_out["Type"] = self["Type"]
        copy_out["Subtype"] = self["Subtype"]
        copy_out["BaseFont"] = self["BaseFont"]
        copy_out["Encoding"] = copy.deepcopy(self["Encoding"], memodict)
        copy_out["DescendantFonts"] = copy.deepcopy(self["DescendantFonts"], memodict)
        if "ToUnicode" in self:
            copy_out["ToUnicode"] = copy.deepcopy(self.get("ToUnicode"), memodict)

        # return
        return copy_out
