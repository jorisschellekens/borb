import copy
from decimal import Decimal
from typing import Optional

from ptext.object.canvas.font.font import Font


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
        return Decimal(0)

    def get_ascent(self) -> Optional[Decimal]:
        return Decimal(0)

    def get_descent(self) -> Optional[Decimal]:
        return Decimal(0)

    def get_font_name(self) -> Optional[str]:
        return None

    def get_missing_character_width(self) -> Decimal:
        return Decimal(0)

    def get_single_character_width(self, character_code: int) -> Optional[Decimal]:
        return Decimal(0)

    def __deepcopy__(self, memodict={}):
        copy_out = CIDFontType0()
        for k in ["Type", "Subtype", "BaseFont"]:
            copy_out[k] = self[k]
        for k in ["CIDSystemInfo", "FontDescriptor"]:
            copy_out[k] = copy.deepcopy(self[k], memodict)
        for k in ["DW", "W", "DW2", "W2", "CIDToGIDMap"]:
            if k in self:
                copy_out[k] = copy.deepcopy(self.get(k), memodict)
        # return
        return copy_out
