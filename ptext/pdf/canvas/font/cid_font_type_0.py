#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    CID-keyed fonts provide a convenient and efficient method for defining multiple-byte character encodings and
    fonts with a large number of glyphs. These capabilities provide great flexibility for representing text in writing
    systems for languages with large character sets, such as Chinese, Japanese, and Korean (CJK).
"""
import copy
from decimal import Decimal
from typing import Optional

from ptext.io.read.types import Name
from ptext.pdf.canvas.font.font import Font


class CIDFontType0(Font):
    """
    CID-keyed fonts provide a convenient and efficient method for defining multiple-byte character encodings and
    fonts with a large number of glyphs. These capabilities provide great flexibility for representing text in writing
    systems for languages with large character sets, such as Chinese, Japanese, and Korean (CJK).

    The CID-keyed font architecture specifies the external representation of certain font programs, called CMap
    and CIDFont files, along with some conventions for combining and using those files. As mentioned earlier, PDF
    does not support the entire CID-keyed font architecture, which is independent of PDF; CID-keyed fonts may be
    used in other environments.

    A Type 0 CIDFont contains glyph descriptions based on CFF
    """

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

    def __deepcopy__(self, memodict={}):
        copy_out = CIDFontType0()
        for k in ["Type", "Subtype", "BaseFont"]:
            copy_out[Name(k)] = self[k]
        for k in ["CIDSystemInfo", "FontDescriptor"]:
            copy_out[Name(k)] = copy.deepcopy(self[k], memodict)
        for k in ["DW", "W", "DW2", "W2", "CIDToGIDMap"]:
            if k in self:
                copy_out[Name(k)] = copy.deepcopy(self.get(k), memodict)
        # return
        return copy_out
