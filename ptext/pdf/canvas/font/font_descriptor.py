import copy

from ptext.io.read.types import Dictionary


class FontDescriptor(Dictionary):
    """
    A font descriptor specifies metrics and other attributes of a simple font or a CIDFont as a whole, as distinct from
    the metrics of individual glyphs. These font metrics provide information that enables a conforming reader to
    synthesize a substitute font or select a similar font when the font program is unavailable. The font descriptor
    may also be used to embed the font program in the PDF file.

    Font descriptors shall not be used with Type 0 fonts. Beginning with PDF 1.5, font descriptors may be used with
    Type 3 fonts.

    A font descriptor is a dictionary whose entries specify various font attributes. The entries common to all font
    descriptors—for both simple fonts and CIDFonts—are listed in Table 122. Additional entries in the font
    descriptor for a CIDFont are described in 9.8.3, "Font Descriptors for CIDFonts". All integer values shall be
    units in glyph space. The conversion from glyph space to text space is described in 9.2.4, "Glyph Positioning
    and Metrics".
    """

    def __deepcopy__(self, memodict={}):
        out = FontDescriptor()
        for key in ["Type", "FontName", "Flags", "ItalicAngle"]:
            out[key] = self[key]
        for key in [
            "FontFamily",
            "FontStretch",
            "FontWeight",
            "Ascent",
            "Descent",
            "Leading",
            "CapHeight",
            "XHeight",
            "StemV",
            "StemH",
            "AvgWidth",
            "MaxWidth",
            "MissingWidth",
            "CharSet",
        ]:
            if key in self:
                out[key] = self[key]
        for key in ["FontBBox", "FontFile", "FontFile2", "FontFile3"]:
            if key in self:
                out[key] = copy.deepcopy(self[key], memodict)
        return out
