#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the bold italic variant of the Courier typeface.

The `CourierBoldItalic` class encapsulates the metrics and characteristics of the Courier Bold Italic typeface,
a widely used monospaced font. This class is primarily used for rendering bold italic text in PDF documents
where the Courier Bold Italic font is required. It provides access to font-specific properties, including
width, height, and character mapping, ensuring accurate text layout and rendering.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class CourierBoldItalic(StandardType1Font):
    """
    Represents the bold italic variant of the Courier typeface.

    The `CourierBoldItalic` class encapsulates the metrics and characteristics of the Courier Bold Italic typeface,
    a widely used monospaced font. This class is primarily used for rendering bold italic text in PDF documents
    where the Courier Bold Italic font is required. It provides access to font-specific properties, including
    width, height, and character mapping, ensuring accurate text layout and rendering.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Courier-BoldOblique font object with its specific attributes.

        The `CourierBoldItalic` class represents the Courier-BoldOblique font,
        a Type1 font with bold and oblique styling.
        This constructor sets the font's base attributes, including its encoding, font type,
        and width for various Unicode characters. The font is primarily used for PDF rendering.

        The Unicode-to-width mapping defines the fixed-width (600 units) for all characters,
        ensuring consistent text alignment and spacing.
        """
        super().__init__()
        self["BaseFont"] = name("Courier-BoldOblique")
        self["Encoding"] = name("WinAnsiEncoding")
        self["Subtype"] = name("Type1")
        self["Type"] = name("Font")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 600, 'exclam': 600, 'quotedbl': 600, 'numbersign': 600, 'dollar': 600, 'percent': 600, 'ampersand': 600, 'quotesingle': 600, 'quoteright': 600, 'parenleft': 600, 'parenright': 600, 'asterisk': 600, 'plus': 600, 'comma': 600, 'hyphen': 600, 'period': 600, 'slash': 600, 'zero': 600, 'one': 600, 'two': 600, 'three': 600, 'four': 600, 'five': 600, 'six': 600, 'seven': 600, 'eight': 600, 'nine': 600, 'colon': 600, 'semicolon': 600, 'less': 600, 'equal': 600, 'greater': 600, 'question': 600, 'at': 600, 'A': 600, 'B': 600, 'C': 600, 'D': 600, 'E': 600, 'F': 600, 'G': 600, 'H': 600, 'I': 600, 'J': 600, 'K': 600, 'L': 600, 'M': 600, 'N': 600, 'O': 600, 'P': 600, 'Q': 600, 'R': 600, 'S': 600, 'T': 600, 'U': 600, 'V': 600, 'W': 600, 'X': 600, 'Y': 600, 'Z': 600, 'bracketleft': 600, 'backslash': 600, 'bracketright': 600, 'asciicircum': 600, 'underscore': 600, 'grave': 600, 'quoteleft': 600, 'a': 600, 'b': 600, 'c': 600, 'd': 600, 'e': 600, 'f': 600, 'g': 600, 'h': 600, 'i': 600, 'j': 600, 'k': 600, 'l': 600, 'm': 600, 'n': 600, 'o': 600, 'p': 600, 'q': 600, 'r': 600, 's': 600, 't': 600, 'u': 600, 'v': 600, 'w': 600, 'x': 600, 'y': 600, 'z': 600, 'braceleft': 600, 'bar': 600, 'braceright': 600, 'asciitilde': 600, 'exclamdown': 600, 'cent': 600, 'sterling': 600, 'fraction': 600, 'yen': 600, 'brokenbar': 600, 'section': 600, 'currency': 600, 'quotedblleft': 600, 'guillemetleft': 600, 'guilsinglleft': 600, 'guilsinglright': 600, 'fi': 600, 'fl': 600, 'endash': 600, 'dagger': 600, 'daggerdbl': 600, 'periodcentered': 600, 'paragraph': 600, 'bullet': 600, 'quotesinglbase': 600, 'quotedblbase': 600, 'quotedblright': 600, 'guillemetright': 600, 'ellipsis': 600, 'perthousand': 600, 'questiondown': 600, 'acute': 600, 'circumflex': 600, 'tilde': 600, 'macron': 600, 'breve': 600, 'dotaccent': 600, 'dieresis': 600, 'ring': 600, 'cedilla': 600, 'hungarumlaut': 600, 'ogonek': 600, 'caron': 600, 'emdash': 600, 'AE': 600, 'ordfeminine': 600, 'Lslash': 600, 'Oslash': 600, 'OE': 600, 'ordmasculine': 600, 'ae': 600, 'dotlessi': 600, 'lslash': 600, 'oslash': 600, 'oe': 600, 'germandbls': 600, 'Idieresis': 600, 'eacute': 600, 'abreve': 600, 'uhungarumlaut': 600, 'ecaron': 600, 'Ydieresis': 600, 'divide': 600, 'Yacute': 600, 'Acircumflex': 600, 'aacute': 600, 'Ucircumflex': 600, 'yacute': 600, 'scommaaccent': 600, 'ecircumflex': 600, 'Uring': 600, 'Udieresis': 600, 'aogonek': 600, 'Uacute': 600, 'uogonek': 600, 'Edieresis': 600, 'Dcroat': 600, 'copyright': 600, 'Emacron': 600, 'ccaron': 600, 'aring': 600, 'Ncommaaccent': 600, 'lacute': 600, 'agrave': 600, 'Tcommaaccent': 600, 'Cacute': 600, 'atilde': 600, 'Edotaccent': 600, 'scaron': 600, 'scedilla': 600, 'iacute': 600, 'lozenge': 600, 'Rcaron': 600, 'Gcommaaccent': 600, 'ucircumflex': 600, 'acircumflex': 600, 'Amacron': 600, 'rcaron': 600, 'ccedilla': 600, 'Zdotaccent': 600, 'Thorn': 600, 'Omacron': 600, 'Racute': 600, 'Sacute': 600, 'dcaron': 600, 'Umacron': 600, 'uring': 600, 'Ograve': 600, 'Agrave': 600, 'Abreve': 600, 'multiply': 600, 'uacute': 600, 'Tcaron': 600, 'partialdiff': 600, 'ydieresis': 600, 'Nacute': 600, 'icircumflex': 600, 'Ecircumflex': 600, 'adieresis': 600, 'edieresis': 600, 'cacute': 600, 'nacute': 600, 'umacron': 600, 'Ncaron': 600, 'Iacute': 600, 'plusminus': 600, 'registered': 600, 'Gbreve': 600, 'Idotaccent': 600, 'summation': 600, 'Egrave': 600, 'racute': 600, 'omacron': 600, 'Zacute': 600, 'Zcaron': 600, 'greaterequal': 600, 'Eth': 600, 'Ccedilla': 600, 'lcommaaccent': 600, 'tcaron': 600, 'eogonek': 600, 'Uogonek': 600, 'Aacute': 600, 'Adieresis': 600, 'egrave': 600, 'zacute': 600, 'iogonek': 600, 'Oacute': 600, 'oacute': 600, 'amacron': 600, 'sacute': 600, 'idieresis': 600, 'Ocircumflex': 600, 'Ugrave': 600, 'Delta': 600, 'thorn': 600, 'Odieresis': 600, 'mu': 600, 'igrave': 600, 'ohungarumlaut': 600, 'Eogonek': 600, 'dcroat': 600, 'threequarters': 600, 'Scedilla': 600, 'lcaron': 600, 'Kcommaaccent': 600, 'Lacute': 600, 'trademark': 600, 'edotaccent': 600, 'Igrave': 600, 'Imacron': 600, 'Lcaron': 600, 'onehalf': 600, 'lessequal': 600, 'ocircumflex': 600, 'ntilde': 600, 'Uhungarumlaut': 600, 'Eacute': 600, 'emacron': 600, 'gbreve': 600, 'onequarter': 600, 'Scaron': 600, 'Scommaaccent': 600, 'Ohungarumlaut': 600, 'degree': 600, 'ograve': 600, 'Ccaron': 600, 'ugrave': 600, 'radical': 600, 'Dcaron': 600, 'rcommaaccent': 600, 'Ntilde': 600, 'otilde': 600, 'Rcommaaccent': 600, 'Lcommaaccent': 600, 'Atilde': 600, 'Aogonek': 600, 'Aring': 600, 'Otilde': 600, 'zdotaccent': 600, 'Ecaron': 600, 'Iogonek': 600, 'kcommaaccent': 600, 'minus': 600, 'Icircumflex': 600, 'ncaron': 600, 'tcommaaccent': 600, 'logicalnot': 600, 'odieresis': 600, 'udieresis': 600, 'notequal': 600, 'gcommaaccent': 600, 'eth': 600, 'zcaron': 600, 'ncommaaccent': 600, 'imacron': 600, 'Euro': 600} # type: ignore[annotation-unchecked]
        # fmt: on

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
        if self.get("FontDescriptor", {}).get("Widths", None) is not None:
            return super().get_width(
                text=text,
                character_spacing=character_spacing,
                font_size=font_size,
                word_spacing=word_spacing,
            )

        # default
        if len(text) == 0:
            return 0
        character_names: typing.List[str] = [
            AdobeGlyphList.ADOBE_CHARACTER_TO_CHARACTER_NAME.get(c, ".notdef")
            for c in text
        ]

        character_width: typing.List[float] = [
            self.__character_name_to_width.get(x, 0) for x in character_names
        ]
        character_width = [w / 1000 for w in character_width]

        # apply character spacing
        character_width = [(w + character_spacing) for w in character_width]
        character_width[-1] -= character_spacing

        # apply word spacing
        character_width = [
            (w + word_spacing) if character_names[i] == "space" else w
            for i, w in enumerate(character_width)
        ]

        # apply font size
        import math

        return math.ceil(sum(character_width) * font_size)
