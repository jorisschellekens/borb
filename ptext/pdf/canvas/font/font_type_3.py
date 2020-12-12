from ptext.pdf.canvas.font.font import Font


class FontType3(Font):
    """
    Type 3 fonts differ from the other fonts supported by PDF. A Type 3 font dictionary defines the font; font
    dictionaries for other fonts simply contain information about the font and refer to a separate font program for the
    actual glyph descriptions. In Type 3 fonts, glyphs shall be defined by streams of PDF graphics operators. These
    streams shall be associated with glyph names. A separate encoding entry shall map character codes to the
    appropriate glyph names for the glyphs.
    """

    pass
