#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the Times Bold Italic typeface and its properties.

The Times Bold Italic class encapsulates the metrics and characteristics of the Times typeface,
a widely used serif font known for its readability and elegance. This class is typically used to
render text in PDF documents where Times Bold Italic is required.

It provides access to font-specific properties such as width, height, and character mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class TimesBoldItalic(StandardType1Font):
    """
    Represents the Times Bold Italic typeface and its properties.

    The Times Bold Italic class encapsulates the metrics and characteristics of the Times typeface,
    a widely used serif font known for its readability and elegance. This class is typically used to
    render text in PDF documents where Times Bold Italic is required.

    It provides access to font-specific properties such as width, height, and character mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Times Bold Italic font object with its specific attributes.

        The `TimesBoldItalic` class represents the Times Bold Italic font,
        combining the features of the Times font with bold and italic styling.
        This constructor sets the font's base attributes, including its encoding, font type,
        and width for various Unicode characters.
        This font is ideal for emphasizing titles and important text within documents.
        """
        super().__init__()
        self["BaseFont"] = name("Times-BoldOblique")
        self["Encoding"] = name("WinAnsiEncoding")
        self["Subtype"] = name("Type1")
        self["Type"] = name("Font")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 250, 'exclam': 389, 'quotedbl': 555, 'numbersign': 500, 'dollar': 500, 'percent': 833, 'ampersand': 778, 'quotesingle': 278, 'parenleft': 333, 'parenright': 333, 'asterisk': 500, 'plus': 570, 'comma': 250, 'hyphen': 333, 'period': 250, 'slash': 278, 'zero': 500, 'one': 500, 'two': 500, 'three': 500, 'four': 500, 'five': 500, 'six': 500, 'seven': 500, 'eight': 500, 'nine': 500, 'colon': 333, 'semicolon': 333, 'less': 570, 'equal': 570, 'greater': 570, 'question': 500, 'at': 832, 'A': 667, 'B': 667, 'C': 667, 'D': 722, 'E': 667, 'F': 667, 'G': 722, 'H': 778, 'I': 389, 'J': 500, 'K': 667, 'L': 611, 'M': 889, 'N': 722, 'O': 722, 'P': 611, 'Q': 722, 'R': 667, 'S': 556, 'T': 611, 'U': 722, 'V': 667, 'W': 889, 'X': 667, 'Y': 611, 'Z': 611, 'bracketleft': 333, 'backslash': 278, 'bracketright': 333, 'asciicircum': 570, 'underscore': 500, 'grave': 333, 'a': 500, 'b': 500, 'c': 444, 'd': 500, 'e': 444, 'f': 333, 'g': 500, 'h': 556, 'i': 278, 'j': 278, 'k': 500, 'l': 278, 'm': 778, 'n': 556, 'o': 500, 'p': 500, 'q': 500, 'r': 389, 's': 389, 't': 278, 'u': 556, 'v': 444, 'w': 667, 'x': 500, 'y': 444, 'z': 389, 'braceleft': 348, 'bar': 220, 'braceright': 348, 'asciitilde': 570, 'exclamdown': 389, 'cent': 500, 'sterling': 500, 'currency': 500, 'yen': 500, 'brokenbar': 220, 'section': 500, 'dieresis': 333, 'copyright': 747, 'ordfeminine': 266, 'guillemetleft': 500, 'logicalnot': 606, 'registered': 747, 'macron': 333, 'degree': 400, 'plusminus': 570, 'acute': 333, 'paragraph': 500, 'periodcentered': 250, 'cedilla': 333, 'ordmasculine': 300, 'guillemetright': 500, 'onequarter': 750, 'onehalf': 750, 'threequarters': 750, 'questiondown': 500, 'Agrave': 667, 'Aacute': 667, 'Acircumflex': 667, 'Atilde': 667, 'Adieresis': 667, 'Aring': 667, 'AE': 944, 'Ccedilla': 667, 'Egrave': 667, 'Eacute': 667, 'Ecircumflex': 667, 'Edieresis': 667, 'Igrave': 389, 'Iacute': 389, 'Icircumflex': 389, 'Idieresis': 389, 'Eth': 722, 'Ntilde': 722, 'Ograve': 722, 'Oacute': 722, 'Ocircumflex': 722, 'Otilde': 722, 'Odieresis': 722, 'multiply': 570, 'Oslash': 722, 'Ugrave': 722, 'Uacute': 722, 'Ucircumflex': 722, 'Udieresis': 722, 'Yacute': 611, 'Thorn': 611, 'germandbls': 500, 'agrave': 500, 'aacute': 500, 'acircumflex': 500, 'atilde': 500, 'adieresis': 500, 'aring': 500, 'ae': 722, 'ccedilla': 444, 'egrave': 444, 'eacute': 444, 'ecircumflex': 444, 'edieresis': 444, 'igrave': 278, 'iacute': 278, 'icircumflex': 278, 'idieresis': 278, 'eth': 500, 'ntilde': 556, 'ograve': 500, 'oacute': 500, 'ocircumflex': 500, 'otilde': 500, 'odieresis': 500, 'divide': 570, 'oslash': 500, 'ugrave': 556, 'uacute': 556, 'ucircumflex': 556, 'udieresis': 556, 'yacute': 444, 'thorn': 500, 'ydieresis': 444, 'Amacron': 667, 'amacron': 500, 'Abreve': 667, 'abreve': 500, 'Aogonek': 667, 'aogonek': 500, 'Cacute': 667, 'cacute': 444, 'Ccaron': 667, 'ccaron': 444, 'Dcaron': 722, 'dcaron': 608, 'Dcroat': 722, 'dcroat': 500, 'Emacron': 667, 'emacron': 444, 'Edotaccent': 667, 'edotaccent': 444, 'Eogonek': 667, 'eogonek': 444, 'Ecaron': 667, 'ecaron': 444, 'Gbreve': 722, 'gbreve': 500, 'Gcommaaccent': 722, 'gcommaaccent': 500, 'Imacron': 389, 'imacron': 278, 'Iogonek': 389, 'iogonek': 278, 'Idotaccent': 389, 'dotlessi': 278, 'Kcommaaccent': 667, 'kcommaaccent': 500, 'Lacute': 611, 'lacute': 278, 'Lcommaaccent': 611, 'lcommaaccent': 278, 'Lcaron': 611, 'lcaron': 382, 'Lslash': 611, 'lslash': 278, 'Nacute': 722, 'nacute': 556, 'Ncommaaccent': 722, 'ncommaaccent': 556, 'Ncaron': 722, 'ncaron': 556, 'Omacron': 722, 'omacron': 500, 'Ohungarumlaut': 722, 'ohungarumlaut': 500, 'OE': 944, 'oe': 722, 'Racute': 667, 'racute': 389, 'Rcommaaccent': 667, 'rcommaaccent': 389, 'Rcaron': 667, 'rcaron': 389, 'Sacute': 556, 'sacute': 389, 'Scedilla': 556, 'scedilla': 389, 'Scaron': 556, 'scaron': 389, 'Tcaron': 611, 'tcaron': 366, 'Umacron': 722, 'umacron': 556, 'Uring': 722, 'uring': 556, 'Uhungarumlaut': 722, 'uhungarumlaut': 556, 'Uogonek': 722, 'uogonek': 556, 'Ydieresis': 611, 'Zacute': 611, 'zacute': 389, 'Zdotaccent': 611, 'zdotaccent': 389, 'Zcaron': 611, 'zcaron': 389, 'Scommaaccent': 556, 'scommaaccent': 389, 'Tcommaaccent': 611, 'tcommaaccent': 278, 'circumflex': 333, 'caron': 333, 'breve': 333, 'dotaccent': 333, 'ring': 333, 'ogonek': 333, 'tilde': 333, 'hungarumlaut': 333, 'Delta': 612, 'mu': 576, 'endash': 500, 'emdash': 1000, 'quoteleft': 333, 'quoteright': 333, 'quotesinglbase': 333, 'quotedblleft': 500, 'quotedblright': 500, 'quotedblbase': 500, 'dagger': 500, 'daggerdbl': 500, 'bullet': 350, 'ellipsis': 1000, 'perthousand': 1000, 'guilsinglleft': 333, 'guilsinglright': 333, 'fraction': 167, 'Euro': 500, 'trademark': 1000, 'partialdiff': 494, 'summation': 600, 'minus': 606, 'radical': 549, 'notequal': 549, 'lessequal': 549, 'greaterequal': 549, 'lozenge': 494, 'fi': 556, 'fl': 556} # type: ignore[annotation-unchecked]
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
