#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a composite font in a PDF.

The `CompositeFont` class is used to represent composite fonts, also known as Type 0 fonts,
in PDF documents. Composite fonts are multi-byte fonts that allow for a large number of
glyphs, making them suitable for representing complex scripts and character sets such as
Chinese, Japanese, and Korean (CJK).

This class builds upon the base `Font` class, providing additional support for handling
CIDFonts and CMaps, which map character codes to glyphs and define character encodings
for composite fonts. Composite fonts are often used in conjunction with encoding schemes
that support wide character sets.
"""

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.cmap import CMap
from borb.pdf.font.composite_font.cid_type_0_font import CIDType0Font
from borb.pdf.font.font import Font


class CompositeFont(Font):
    """
    Represents a composite font in a PDF.

    The `CompositeFont` class is used to represent composite fonts, also known as Type 0 fonts,
    in PDF documents. Composite fonts are multi-byte fonts that allow for a large number of
    glyphs, making them suitable for representing complex scripts and character sets such as
    Chinese, Japanese, and Korean (CJK).

    This class builds upon the base `Font` class, providing additional support for handling
    CIDFonts and CMaps, which map character codes to glyphs and define character encodings
    for composite fonts. Composite fonts are often used in conjunction with encoding schemes
    that support wide character sets.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_width(
        self,
        text: str,
        character_spacing: float = 0,
        font_size: float = 12,
        word_spacing: float = 0,
    ) -> int:
        """
        Return the total width of a text string when rendered with the font at a specific size.

        This function calculates the width of the given text string when rendered with the font
        at the specified font size.

        :param font_size:           The font size to be used for rendering.
        :param text:                The text string to calculate the width for.
        :param word_spacing:        The word spacing to be used for rendering
        :param character_spacing:   The character spacing to be used for rendering
        :return:                    The width (in points) of the text in the specified font size.
        """
        descendant_font: CIDType0Font = self["DescendantFonts"][0]

        # CMap
        cmap: CMap = self["ToUnicode"]

        # delegate to DescendantFonts
        return descendant_font.get_width(
            text=[
                (
                    cmap.get_character_code(c),
                    AdobeGlyphList.ADOBE_CHARACTER_TO_CHARACTER_NAME.get(c, ".notdef"),
                )
                for c in text
            ],
            character_spacing=character_spacing,
            font_size=font_size,
            word_spacing=word_spacing,
        )
