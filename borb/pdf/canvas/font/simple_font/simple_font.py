#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
There are several types of simple fonts, all of which have these properties:

•   Glyphs in the font shall be selected by single-byte character codes obtained from a string that is shown by
    the text-showing operators. Logically, these codes index into a table of 256 glyphs; the mapping from
    codes to glyphs is called the font’s encoding. Under some circumstances, the encoding may be altered by
    means described in 9.6.6, "Character Encoding".

•   Each glyph shall have a single set of metrics, including a horizontal displacement or width, as described in
    9.2.4, "Glyph Positioning and Metrics"; that is, simple fonts support only horizontal writing mode.

•   Except for Type 0 fonts, Type 3 fonts in non-Tagged PDF documents, and certain standard Type 1 fonts,
    every font dictionary shall contain a subsidiary dictionary, the font descriptor, containing font-wide metrics
    and other attributes of the font; see 9.8, "Font Descriptors". Among those attributes is an optional font file
    stream containing the font program.
"""
from borb.pdf.canvas.font.font import Font


class SimpleFont(Font):
    """
    There are several types of simple fonts, all of which have these properties:

    •   Glyphs in the font shall be selected by single-byte character codes obtained from a string that is shown by
        the text-showing operators. Logically, these codes index into a table of 256 glyphs; the mapping from
        codes to glyphs is called the font’s encoding. Under some circumstances, the encoding may be altered by
        means described in 9.6.6, "Character Encoding".

    •   Each glyph shall have a single set of metrics, including a horizontal displacement or width, as described in
        9.2.4, "Glyph Positioning and Metrics"; that is, simple fonts support only horizontal writing mode.

    •   Except for Type 0 fonts, Type 3 fonts in non-Tagged PDF documents, and certain standard Type 1 fonts,
        every font dictionary shall contain a subsidiary dictionary, the font descriptor, containing font-wide metrics
        and other attributes of the font; see 9.8, "Font Descriptors". Among those attributes is an optional font file
        stream containing the font program.
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
    pass
