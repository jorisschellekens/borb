#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the Times Italic typeface and its properties.

The Times Italic class encapsulates the metrics and characteristics of the Times typeface,
a widely used serif font known for its readability and elegance. This class is typically used to
render text in PDF documents where Times Italic is required.

It provides access to font-specific properties such as width, height, and character mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class TimesItalic(StandardType1Font):
    """
    Represents the Times Italic typeface and its properties.

    The Times Italic class encapsulates the metrics and characteristics of the Times typeface,
    a widely used serif font known for its readability and elegance. This class is typically used to
    render text in PDF documents where Times Italic is required.

    It provides access to font-specific properties such as width, height, and character mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Times Italic font object with its specific attributes.

        The `TimesItalic` class represents the Times Italic font,
        providing an italicized version of the classic Times font.
        This constructor sets the font's base attributes, including its encoding, font type,
        and width for various Unicode characters.
        The italic style is often used for emphasis, making it suitable for citations and stylistic text.
        """
        super().__init__()
        self["BaseFont"] = name("Times-Italic")
        self["Encoding"] = name("WinAnsiEncoding")
        self["Subtype"] = name("Type1")
        self["Type"] = name("Font")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 250, 'exclam': 333, 'quotedbl': 420, 'numbersign': 500, 'dollar': 500, 'percent': 833, 'ampersand': 778, 'quotesingle': 214, 'parenleft': 333, 'parenright': 333, 'asterisk': 500, 'plus': 675, 'comma': 250, 'hyphen': 333, 'period': 250, 'slash': 278, 'zero': 500, 'one': 500, 'two': 500, 'three': 500, 'four': 500, 'five': 500, 'six': 500, 'seven': 500, 'eight': 500, 'nine': 500, 'colon': 333, 'semicolon': 333, 'less': 675, 'equal': 675, 'greater': 675, 'question': 500, 'at': 920, 'A': 611, 'B': 611, 'C': 667, 'D': 722, 'E': 611, 'F': 611, 'G': 722, 'H': 722, 'I': 333, 'J': 444, 'K': 667, 'L': 556, 'M': 833, 'N': 667, 'O': 722, 'P': 611, 'Q': 722, 'R': 611, 'S': 500, 'T': 556, 'U': 722, 'V': 611, 'W': 833, 'X': 611, 'Y': 556, 'Z': 556, 'bracketleft': 389, 'backslash': 278, 'bracketright': 389, 'asciicircum': 422, 'underscore': 500, 'grave': 333, 'a': 500, 'b': 500, 'c': 444, 'd': 500, 'e': 444, 'f': 278, 'g': 500, 'h': 500, 'i': 278, 'j': 278, 'k': 444, 'l': 278, 'm': 722, 'n': 500, 'o': 500, 'p': 500, 'q': 500, 'r': 389, 's': 389, 't': 278, 'u': 500, 'v': 444, 'w': 667, 'x': 444, 'y': 444, 'z': 389, 'braceleft': 400, 'bar': 275, 'braceright': 400, 'asciitilde': 541, 'exclamdown': 389, 'cent': 500, 'sterling': 500, 'currency': 500, 'yen': 500, 'brokenbar': 275, 'section': 500, 'dieresis': 333, 'copyright': 760, 'ordfeminine': 276, 'guillemetleft': 500, 'logicalnot': 675, 'registered': 760, 'macron': 333, 'degree': 400, 'plusminus': 675, 'acute': 333, 'paragraph': 523, 'periodcentered': 250, 'cedilla': 333, 'ordmasculine': 310, 'guillemetright': 500, 'onequarter': 750, 'onehalf': 750, 'threequarters': 750, 'questiondown': 500, 'Agrave': 611, 'Aacute': 611, 'Acircumflex': 611, 'Atilde': 611, 'Adieresis': 611, 'Aring': 611, 'AE': 889, 'Ccedilla': 667, 'Egrave': 611, 'Eacute': 611, 'Ecircumflex': 611, 'Edieresis': 611, 'Igrave': 333, 'Iacute': 333, 'Icircumflex': 333, 'Idieresis': 333, 'Eth': 722, 'Ntilde': 667, 'Ograve': 722, 'Oacute': 722, 'Ocircumflex': 722, 'Otilde': 722, 'Odieresis': 722, 'multiply': 675, 'Oslash': 722, 'Ugrave': 722, 'Uacute': 722, 'Ucircumflex': 722, 'Udieresis': 722, 'Yacute': 556, 'Thorn': 611, 'germandbls': 500, 'agrave': 500, 'aacute': 500, 'acircumflex': 500, 'atilde': 500, 'adieresis': 500, 'aring': 500, 'ae': 667, 'ccedilla': 444, 'egrave': 444, 'eacute': 444, 'ecircumflex': 444, 'edieresis': 444, 'igrave': 278, 'iacute': 278, 'icircumflex': 278, 'idieresis': 278, 'eth': 500, 'ntilde': 500, 'ograve': 500, 'oacute': 500, 'ocircumflex': 500, 'otilde': 500, 'odieresis': 500, 'divide': 675, 'oslash': 500, 'ugrave': 500, 'uacute': 500, 'ucircumflex': 500, 'udieresis': 500, 'yacute': 444, 'thorn': 500, 'ydieresis': 444, 'Amacron': 611, 'amacron': 500, 'Abreve': 611, 'abreve': 500, 'Aogonek': 611, 'aogonek': 500, 'Cacute': 667, 'cacute': 444, 'Ccaron': 667, 'ccaron': 444, 'Dcaron': 722, 'dcaron': 544, 'Dcroat': 722, 'dcroat': 500, 'Emacron': 611, 'emacron': 444, 'Edotaccent': 611, 'edotaccent': 444, 'Eogonek': 611, 'eogonek': 444, 'Ecaron': 611, 'ecaron': 444, 'Gbreve': 722, 'gbreve': 500, 'Gcommaaccent': 722, 'gcommaaccent': 500, 'Imacron': 333, 'imacron': 278, 'Iogonek': 333, 'iogonek': 278, 'Idotaccent': 333, 'dotlessi': 278, 'Kcommaaccent': 667, 'kcommaaccent': 444, 'Lacute': 556, 'lacute': 278, 'Lcommaaccent': 556, 'lcommaaccent': 278, 'Lcaron': 611, 'lcaron': 300, 'Lslash': 556, 'lslash': 278, 'Nacute': 667, 'nacute': 500, 'Ncommaaccent': 667, 'ncommaaccent': 500, 'Ncaron': 667, 'ncaron': 500, 'Omacron': 722, 'omacron': 500, 'Ohungarumlaut': 722, 'ohungarumlaut': 500, 'OE': 944, 'oe': 667, 'Racute': 611, 'racute': 389, 'Rcommaaccent': 611, 'rcommaaccent': 389, 'Rcaron': 611, 'rcaron': 389, 'Sacute': 500, 'sacute': 389, 'Scedilla': 500, 'scedilla': 389, 'Scaron': 500, 'scaron': 389, 'Tcaron': 556, 'tcaron': 300, 'Umacron': 722, 'umacron': 500, 'Uring': 722, 'uring': 500, 'Uhungarumlaut': 722, 'uhungarumlaut': 500, 'Uogonek': 722, 'uogonek': 500, 'Ydieresis': 556, 'Zacute': 556, 'zacute': 389, 'Zdotaccent': 556, 'zdotaccent': 389, 'Zcaron': 556, 'zcaron': 389, 'Scommaaccent': 500, 'scommaaccent': 389, 'Tcommaaccent': 556, 'tcommaaccent': 278, 'circumflex': 333, 'caron': 333, 'breve': 333, 'dotaccent': 333, 'ring': 333, 'ogonek': 333, 'tilde': 333, 'hungarumlaut': 333, 'Delta': 612, 'mu': 500, 'endash': 500, 'emdash': 889, 'quoteleft': 333, 'quoteright': 333, 'quotesinglbase': 333, 'quotedblleft': 556, 'quotedblright': 556, 'quotedblbase': 556, 'dagger': 500, 'daggerdbl': 500, 'bullet': 350, 'ellipsis': 889, 'perthousand': 1000, 'guilsinglleft': 333, 'guilsinglright': 333, 'fraction': 167, 'Euro': 500, 'trademark': 980, 'partialdiff': 476, 'summation': 600, 'minus': 675, 'radical': 453, 'notequal': 549, 'lessequal': 549, 'greaterequal': 549, 'lozenge': 471, 'fi': 500, 'fl': 500} # type: ignore[annotation-unchecked]
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
