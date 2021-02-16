# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A composite font, also called a Type 0 font, is one whose glyphs are obtained from a fontlike object called a
    CIDFont. A composite font shall be represented by a font dictionary whose Subtype value is Type0. The Type
    0 font is known as the root font, and its associated CIDFont is called its descendant.
"""
import copy
from decimal import Decimal
from typing import Optional

from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.font.glyph_line import GlyphLine


class FontType0(Font):
    """
    A composite font, also called a Type 0 font, is one whose glyphs are obtained from a fontlike object called a
    CIDFont. A composite font shall be represented by a font dictionary whose Subtype value is Type0. The Type
    0 font is known as the root font, and its associated CIDFont is called its descendant.
    """

    def get_average_character_width(self) -> Optional[Decimal]:
        """
        (Optional) The average width of glyphs in the font. Default value: 0.
        """
        return self.get_descendant_font().get_average_character_width()

    def get_ascent(self) -> Optional[Decimal]:
        """
        (Required, except for Type 3 fonts) The maximum height above the
        baseline reached by glyphs in this font. The height of glyphs for
        accented characters shall be excluded.
        """
        return self.get_descendant_font().get_ascent()

    def get_descent(self) -> Optional[Decimal]:
        """
        (Required, except for Type 3 fonts) The maximum depth below the
        baseline reached by glyphs in this font. The value shall be a negative
        number.
        """
        return self.get_descendant_font().get_descent()

    def get_single_character_width(self, character_code: int) -> Optional[Decimal]:
        """
        Get the width (in text space) of a given character code.
        Returns None if the character code can not be represented in this Font.
        """
        return self.get_descendant_font().get_single_character_width(character_code)

    def get_missing_character_width(self) -> Decimal:
        """
        (Optional) The width to use for character codes whose widths are not
        specified in a font dictionary’s Widths array. This shall have a
        predictable effect only if all such codes map to glyphs whose actual
        widths are the same as the value of the MissingWidth entry. Default
        value: 0.
        """
        return self.get_descendant_font().get_missing_character_width()

    def get_font_name(self) -> Optional[str]:
        """
        (Required) The PostScript name of the font. For Type 1 fonts, this is
        always the value of the FontName entry in the font program; for more
        information, see Section 5.2 of the PostScript Language Reference,
        Third Edition. The PostScript name of the font may be used to find the
        font program in the conforming reader or its environment. It is also the
        name that is used when printing to a PostScript output device.
        """
        return self.get_descendant_font().get_font_name()

    def get_descendant_font(self) -> Font:
        assert "DescendantFonts" in self
        if isinstance(self["DescendantFonts"], list):
            assert isinstance(self["DescendantFonts"][0], Font)
            return self["DescendantFonts"][0]
        if isinstance(self["DescendantFonts"], Font):
            return self["DescendantFonts"]
        assert False

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
