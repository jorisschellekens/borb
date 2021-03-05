#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module defines glyps and glyplines.
    In typography, a glyph /ɡlɪf/ is an elemental symbol within an agreed set of symbols,
    intended to represent a readable character for the purposes of writing.
    Glyphs are considered to be unique marks that collectively add up to the spelling
    of a word or contribute to a specific meaning of what is written,
    with that meaning dependent on cultural and social usage.
"""
from decimal import Decimal
from typing import List, Optional, Union


class Glyph:
    """
    In typography, a glyph /ɡlɪf/ is an elemental symbol within an agreed set of symbols,
    intended to represent a readable character for the purposes of writing.
    Glyphs are considered to be unique marks that collectively add up to the spelling
    of a word or contribute to a specific meaning of what is written,
    with that meaning dependent on cultural and social usage.
    """

    def __init__(
        self, code: int, unicode: Union[int, List[int]], width: Optional[Decimal]
    ):
        self.code = code
        self.width = width if width is not None else Decimal(0)
        self.unicode = unicode
        if self.unicode == 0:
            self.width = Decimal(0)

    def to_unicode_string(self) -> str:
        if isinstance(self.unicode, int) and self.unicode > 0:
            return chr(self.unicode)
        elif isinstance(self.unicode, tuple):
            "".join([chr(x) if x > 0 else "" for x in self.unicode])
        return ""


class GlyphLine:
    def __init__(self, glyphs: List[Glyph]):
        self.glyphs = glyphs

    def get_text(self):
        return "".join([g.to_unicode_string() for g in self.glyphs])

    def to_unicode_string(self, start: Optional[int] = None, end: Optional[int] = None):
        start = start or 0
        end = end or -1
        return "".join([self.glyphs[i].to_unicode_string() for i in range(start, end)])

    def append(self, glyph: Glyph) -> "GlyphLine":
        self.glyphs.append(glyph)
        return self

    def append_glyph_line(self, glyph_line: "GlyphLine") -> "GlyphLine":
        for g in glyph_line.glyphs:
            self.glyphs.append(g)
        return self

    def get_width_in_text_space(
        self,
        font_size: Decimal,
        character_spacing: Decimal = Decimal(0),
        word_spacing: Decimal = Decimal(0),
        horizontal_scaling: Decimal = Decimal(100),
    ) -> Decimal:
        """
        Get the width of a String in text space units
        """
        total_width = Decimal(0)
        for g in self.glyphs:
            character_width = Decimal(g.width) * font_size * Decimal(0.001)

            # add word spacing where applicable
            if g.unicode == " ":
                character_width += word_spacing

            # horizontal scaling
            character_width *= horizontal_scaling / Decimal(100)

            # add character spacing to character_width
            character_width += character_spacing

            # add character width to total
            total_width += character_width

        # subtract character spacing once (there are only N-1 spacings in a string of N characters)
        total_width -= character_spacing

        # return
        return total_width

    def __len__(self):
        return len(self.glyphs)

    def __iter__(self):
        return self.glyphs.__iter__()
