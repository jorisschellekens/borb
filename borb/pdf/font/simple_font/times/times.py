#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the Times typeface and its properties.

The Times typeface is a widely used serif font known for its readability and classic
appearance. This class is typically used to render text in PDF documents where the
Times font is required.

It provides access to font-specific properties such as width, height, and character
mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class Times(StandardType1Font):
    """
    Represents the Times typeface and its properties.

    The Times typeface is a widely used serif font known for its readability and classic
    appearance. This class is typically used to render text in PDF documents where the
    Times font is required.

    It provides access to font-specific properties such as width, height, and character
    mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Times font object with its specific attributes.

        The `Times` class represents the Times font, a Type1 font known for its readability and classic serif design.
        This constructor sets the font's base attributes, including its encoding, font type,
        and width for various Unicode characters.
        The font is widely used in print media, making it suitable for body text and formal documents.
        """
        super().__init__()
        self["BaseFont"] = name("Times-Roman")
        self["Encoding"] = name("WinAnsiEncoding")
        self["Subtype"] = name("Type1")
        self["Type"] = name("Font")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 250, 'exclam': 333, 'quotedbl': 408, 'numbersign': 500, 'dollar': 500, 'percent': 833, 'ampersand': 778, 'quotesingle': 180, 'quoteright': 333, 'parenleft': 333, 'parenright': 333, 'asterisk': 500, 'plus': 564, 'comma': 250, 'hyphen': 333, 'period': 250, 'slash': 278, 'zero': 500, 'one': 500, 'two': 500, 'three': 500, 'four': 500, 'five': 500, 'six': 500, 'seven': 500, 'eight': 500, 'nine': 500, 'colon': 278, 'semicolon': 278, 'less': 564, 'equal': 564, 'greater': 564, 'question': 444, 'at': 921, 'A': 722, 'B': 667, 'C': 667, 'D': 722, 'E': 611, 'F': 556, 'G': 722, 'H': 722, 'I': 333, 'J': 389, 'K': 722, 'L': 611, 'M': 889, 'N': 722, 'O': 722, 'P': 556, 'Q': 722, 'R': 667, 'S': 556, 'T': 611, 'U': 722, 'V': 722, 'W': 944, 'X': 722, 'Y': 722, 'Z': 611, 'bracketleft': 333, 'backslash': 278, 'bracketright': 333, 'asciicircum': 469, 'underscore': 500, 'grave': 333, 'quoteleft': 333, 'a': 444, 'b': 500, 'c': 444, 'd': 500, 'e': 444, 'f': 333, 'g': 500, 'h': 500, 'i': 278, 'j': 278, 'k': 500, 'l': 278, 'm': 778, 'n': 500, 'o': 500, 'p': 500, 'q': 500, 'r': 333, 's': 389, 't': 278, 'u': 500, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 444, 'braceleft': 480, 'bar': 200, 'braceright': 480, 'asciitilde': 541, 'exclamdown': 333, 'cent': 500, 'sterling': 500, 'fraction': 167, 'yen': 500, 'brokenbar': 200, 'section': 500, 'currency': 500, 'quotedblleft': 444, 'guillemetleft': 500, 'guilsinglleft': 333, 'guilsinglright': 333, 'fi': 556, 'fl': 556, 'endash': 500, 'dagger': 500, 'daggerdbl': 500, 'periodcentered': 250, 'paragraph': 453, 'bullet': 350, 'quotesinglbase': 333, 'quotedblbase': 444, 'quotedblright': 444, 'guillemetright': 500, 'ellipsis': 1000, 'perthousand': 1000, 'questiondown': 444, 'acute': 333, 'circumflex': 333, 'tilde': 333, 'macron': 333, 'breve': 333, 'dotaccent': 333, 'dieresis': 333, 'ring': 333, 'cedilla': 333, 'hungarumlaut': 333, 'ogonek': 333, 'caron': 333, 'emdash': 1000, 'AE': 889, 'ordfeminine': 276, 'Lslash': 611, 'Oslash': 722, 'OE': 889, 'ordmasculine': 310, 'ae': 667, 'dotlessi': 278, 'lslash': 278, 'oslash': 500, 'oe': 722, 'germandbls': 500, 'Idieresis': 333, 'eacute': 444, 'abreve': 444, 'uhungarumlaut': 500, 'ecaron': 444, 'Ydieresis': 722, 'divide': 564, 'Yacute': 722, 'Acircumflex': 722, 'aacute': 444, 'Ucircumflex': 722, 'yacute': 500, 'scommaaccent': 389, 'ecircumflex': 444, 'Uring': 722, 'Udieresis': 722, 'aogonek': 444, 'Uacute': 722, 'uogonek': 500, 'Edieresis': 611, 'Dcroat': 722, 'copyright': 760, 'Emacron': 611, 'ccaron': 444, 'aring': 444, 'Ncommaaccent': 722, 'lacute': 278, 'agrave': 444, 'Tcommaaccent': 611, 'Cacute': 667, 'atilde': 444, 'Edotaccent': 611, 'scaron': 389, 'scedilla': 389, 'iacute': 278, 'lozenge': 471, 'Rcaron': 667, 'Gcommaaccent': 722, 'ucircumflex': 500, 'acircumflex': 444, 'Amacron': 722, 'rcaron': 333, 'ccedilla': 444, 'Zdotaccent': 611, 'Thorn': 556, 'Omacron': 722, 'Racute': 667, 'Sacute': 556, 'dcaron': 588, 'Umacron': 722, 'uring': 500, 'Ograve': 722, 'Agrave': 722, 'Abreve': 722, 'multiply': 564, 'uacute': 500, 'Tcaron': 611, 'partialdiff': 476, 'ydieresis': 500, 'Nacute': 722, 'icircumflex': 278, 'Ecircumflex': 611, 'adieresis': 444, 'edieresis': 444, 'cacute': 444, 'nacute': 500, 'umacron': 500, 'Ncaron': 722, 'Iacute': 333, 'plusminus': 564, 'registered': 760, 'Gbreve': 722, 'Idotaccent': 333, 'summation': 600, 'Egrave': 611, 'racute': 333, 'omacron': 500, 'Zacute': 611, 'Zcaron': 611, 'greaterequal': 549, 'Eth': 722, 'Ccedilla': 667, 'lcommaaccent': 278, 'tcaron': 326, 'eogonek': 444, 'Uogonek': 722, 'Aacute': 722, 'Adieresis': 722, 'egrave': 444, 'zacute': 444, 'iogonek': 278, 'Oacute': 722, 'oacute': 500, 'amacron': 444, 'sacute': 389, 'idieresis': 278, 'Ocircumflex': 722, 'Ugrave': 722, 'Delta': 612, 'thorn': 500, 'Odieresis': 722, 'mu': 500, 'igrave': 278, 'ohungarumlaut': 500, 'Eogonek': 611, 'dcroat': 500, 'threequarters': 750, 'Scedilla': 556, 'lcaron': 344, 'Kcommaaccent': 722, 'Lacute': 611, 'trademark': 980, 'edotaccent': 444, 'Igrave': 333, 'Imacron': 333, 'Lcaron': 611, 'onehalf': 750, 'lessequal': 549, 'ocircumflex': 500, 'ntilde': 500, 'Uhungarumlaut': 722, 'Eacute': 611, 'emacron': 444, 'gbreve': 500, 'onequarter': 750, 'Scaron': 556, 'Scommaaccent': 556, 'Ohungarumlaut': 722, 'degree': 400, 'ograve': 500, 'Ccaron': 667, 'ugrave': 500, 'radical': 453, 'Dcaron': 722, 'rcommaaccent': 333, 'Ntilde': 722, 'otilde': 500, 'Rcommaaccent': 667, 'Lcommaaccent': 611, 'Atilde': 722, 'Aogonek': 722, 'Aring': 722, 'Otilde': 722, 'zdotaccent': 444, 'Ecaron': 611, 'Iogonek': 333, 'kcommaaccent': 500, 'minus': 564, 'Icircumflex': 333, 'ncaron': 500, 'tcommaaccent': 278, 'logicalnot': 564, 'odieresis': 500, 'udieresis': 500, 'notequal': 549, 'gcommaaccent': 500, 'eth': 500, 'zcaron': 444, 'ncommaaccent': 500, 'imacron': 278, 'Euro': 500} # type: ignore[annotation-unchecked]
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
