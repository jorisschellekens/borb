from decimal import Decimal
from typing import List, Optional, Union


class Glyph:
    def __init__(
        self, code: int, unicode: Union[int, List[int]], width: Optional[Decimal]
    ):
        self.code = code
        self.width = width if width is not None else Decimal(0)
        self.unicode = unicode

    def to_unicode_string(self) -> str:
        if isinstance(self.unicode, int) and self.unicode >= 0:
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
        return "".join([self.glyphs[i].to_unicode_string() for i in range(start, end)])

    def append(self, glyph: Glyph) -> "GlyphLine":
        self.glyphs.append(glyph)
        return self

    def append_glyph_line(self, glyph_line: "GlyphLine") -> "GlyphLine":
        for g in glyph_line.glyphs:
            self.glyphs.append(g)
        return self

    def __len__(self):
        return len(self.glyphs)

    def __iter__(self):
        return self.glyphs.__iter__()
