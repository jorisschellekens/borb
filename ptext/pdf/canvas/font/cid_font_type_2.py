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
from ptext.pdf.canvas.font.glyph_line import GlyphLine
from ptext.pdf.canvas.font.true_type_font import TrueTypeFont


class CIDFontType2(TrueTypeFont):
    """
    CID-keyed fonts provide a convenient and efficient method for defining multiple-byte character encodings and
    fonts with a large number of glyphs. These capabilities provide great flexibility for representing text in writing
    systems for languages with large character sets, such as Chinese, Japanese, and Korean (CJK).

    The CID-keyed font architecture specifies the external representation of certain font programs, called CMap
    and CIDFont files, along with some conventions for combining and using those files. As mentioned earlier, PDF
    does not support the entire CID-keyed font architecture, which is independent of PDF; CID-keyed fonts may be
    used in other environments.

    A Type 2 CIDFont contains glyph descriptions based on the TrueType font format
    """

    def __init__(self):
        super(CIDFontType2, self).__init__()
        self._cached_widths = None

    def get_single_character_width(self, character_code: int) -> Optional[Decimal]:
        """
        Get the width (in text space) of a given character code.
        Returns None if the character code can not be represented in this Font.
        """
        if "W" not in self:
            if "DW" not in self:
                self[Name("DW")] = Decimal(1000)
            return self["DW"]
        if self._cached_widths is None:
            i = 0
            self._cached_widths = {}
            while i < len(self["W"]):
                c_first = int(self["W"][i])
                if isinstance(self["W"][i + 1], list):
                    for j in range(0, len(self["W"][i + 1])):
                        self._cached_widths[c_first + j] = self["W"][i + 1][j]
                    i += 2
                    continue
                if isinstance(self["W"][i + 1], Decimal):
                    c_last = int(self["W"][i + 1])
                    w = int(self["W"][i + 2])
                    for j in range(c_first, c_last + 1):
                        self._cached_widths[j] = w
                    i += 3
                    continue
        # use cache
        if character_code in self._cached_widths:
            return self._cached_widths[character_code]
        # default
        return None

    def build_glyph_line(self, content) -> GlyphLine:

        # init Encoding
        if self._font_encoding is None:
            self._init_font_encoding()
        if self._font_encoding is None:
            self._font_encoding = self.get_parent()._font_encoding  # type: ignore [attr-defined]

        # init ToUnicode
        if self._to_unicode_map is None:
            self._init_to_unicode_map()
        if self._to_unicode_map is None:
            self._to_unicode_map = self.get_parent()._to_unicode_map  # type: ignore [attr-defined]

        return super().build_glyph_line(content)

    def __deepcopy__(self, memodict={}):
        copy_out = CIDFontType2()
        for k in ["Type", "Subtype", "BaseFont"]:
            copy_out[Name(k)] = self[k]
        for k in ["Name", "FirstChar", "LastChar"]:
            if k in self:
                copy_out[Name(k)] = self.get(k)
        for k in ["Widths", "FontDescriptor", "Encoding", "ToUnicode"]:
            if k in self:
                copy_out[Name(k)] = copy.deepcopy(self.get(k), memodict)
        # return
        return copy_out
