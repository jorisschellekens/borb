#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the Helvetica typeface and its properties.

The `Helvetica` class encapsulates the metrics and characteristics of the Helvetica typeface,
a widely used sans-serif font known for its clean and modern appearance.
This class is typically used to render text in PDF documents where Helvetica
is required. It provides access to font-specific properties such as width,
height, and character mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class Helvetica(StandardType1Font):
    """
    Represents the Helvetica typeface and its properties.

    The `Helvetica` class encapsulates the metrics and characteristics of the Helvetica typeface,
    a widely used sans-serif font known for its clean and modern appearance.
    This class is typically used to render text in PDF documents where Helvetica
    is required. It provides access to font-specific properties such as width,
    height, and character mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Helvetica font object with its specific attributes.

        The `Helvetica` class represents the Helvetica font,
        a widely used sans-serif Type1 font known for its clean and modern appearance.
        This constructor sets the font's base attributes, including its encoding, font type,
        and width for various Unicode characters.
        The font provides proportional spacing, making it suitable for a wide range of text content in PDF rendering.
        """
        super().__init__()
        self["BaseFont"] = name("Helvetica")
        self["Encoding"] = name("WinAnsiEncoding")
        self["Subtype"] = name("Type1")
        self["Type"] = name("Font")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 278, 'exclam': 278, 'quotedbl': 355, 'numbersign': 556, 'dollar': 556, 'percent': 889, 'ampersand': 667, 'quotesingle': 191, 'quoteright': 222, 'parenleft': 333, 'parenright': 333, 'asterisk': 389, 'plus': 584, 'comma': 278, 'hyphen': 333, 'period': 278, 'slash': 278, 'zero': 556, 'one': 556, 'two': 556, 'three': 556, 'four': 556, 'five': 556, 'six': 556, 'seven': 556, 'eight': 556, 'nine': 556, 'colon': 278, 'semicolon': 278, 'less': 584, 'equal': 584, 'greater': 584, 'question': 556, 'at': 1015, 'A': 667, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 722, 'I': 278, 'J': 500, 'K': 667, 'L': 556, 'M': 833, 'N': 722, 'O': 778, 'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944, 'X': 667, 'Y': 667, 'Z': 611, 'bracketleft': 278, 'backslash': 278, 'bracketright': 278, 'asciicircum': 469, 'underscore': 556, 'grave': 333, 'quoteleft': 222, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556, 'f': 278, 'g': 556, 'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222, 'm': 833, 'n': 556, 'o': 556, 'p': 556, 'q': 556, 'r': 333, 's': 500, 't': 278, 'u': 556, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 500, 'braceleft': 334, 'bar': 260, 'braceright': 334, 'asciitilde': 584, 'exclamdown': 333, 'cent': 556, 'sterling': 556, 'fraction': 167, 'yen': 556, 'brokenbar': 260, 'section': 556, 'currency': 556, 'quotedblleft': 333, 'guillemetleft': 556, 'guilsinglleft': 333, 'guilsinglright': 333, 'fi': 500, 'fl': 500, 'endash': 556, 'dagger': 556, 'daggerdbl': 556, 'periodcentered': 278, 'paragraph': 537, 'bullet': 350, 'quotesinglbase': 222, 'quotedblbase': 333, 'quotedblright': 333, 'guillemetright': 556, 'ellipsis': 1000, 'perthousand': 1000, 'questiondown': 611, 'acute': 333, 'circumflex': 333, 'tilde': 333, 'macron': 333, 'breve': 333, 'dotaccent': 333, 'dieresis': 333, 'ring': 333, 'cedilla': 333, 'hungarumlaut': 333, 'ogonek': 333, 'caron': 333, 'emdash': 1000, 'AE': 1000, 'ordfeminine': 370, 'Lslash': 556, 'Oslash': 778, 'OE': 1000, 'ordmasculine': 365, 'ae': 889, 'dotlessi': 278, 'lslash': 222, 'oslash': 611, 'oe': 944, 'germandbls': 611, 'Idieresis': 278, 'eacute': 556, 'abreve': 556, 'uhungarumlaut': 556, 'ecaron': 556, 'Ydieresis': 667, 'divide': 584, 'Yacute': 667, 'Acircumflex': 667, 'aacute': 556, 'Ucircumflex': 722, 'yacute': 500, 'scommaaccent': 500, 'ecircumflex': 556, 'Uring': 722, 'Udieresis': 722, 'aogonek': 556, 'Uacute': 722, 'uogonek': 556, 'Edieresis': 667, 'Dcroat': 722, 'copyright': 737, 'Emacron': 667, 'ccaron': 500, 'aring': 556, 'Ncommaaccent': 722, 'lacute': 222, 'agrave': 556, 'Tcommaaccent': 611, 'Cacute': 722, 'atilde': 556, 'Edotaccent': 667, 'scaron': 500, 'scedilla': 500, 'iacute': 278, 'lozenge': 471, 'Rcaron': 722, 'Gcommaaccent': 778, 'ucircumflex': 556, 'acircumflex': 556, 'Amacron': 667, 'rcaron': 333, 'ccedilla': 500, 'Zdotaccent': 611, 'Thorn': 667, 'Omacron': 778, 'Racute': 722, 'Sacute': 667, 'dcaron': 643, 'Umacron': 722, 'uring': 556, 'Ograve': 778, 'Agrave': 667, 'Abreve': 667, 'multiply': 584, 'uacute': 556, 'Tcaron': 611, 'partialdiff': 476, 'ydieresis': 500, 'Nacute': 722, 'icircumflex': 278, 'Ecircumflex': 667, 'adieresis': 556, 'edieresis': 556, 'cacute': 500, 'nacute': 556, 'umacron': 556, 'Ncaron': 722, 'Iacute': 278, 'plusminus': 584, 'registered': 737, 'Gbreve': 778, 'Idotaccent': 278, 'summation': 600, 'Egrave': 667, 'racute': 333, 'omacron': 556, 'Zacute': 611, 'Zcaron': 611, 'greaterequal': 549, 'Eth': 722, 'Ccedilla': 722, 'lcommaaccent': 222, 'tcaron': 317, 'eogonek': 556, 'Uogonek': 722, 'Aacute': 667, 'Adieresis': 667, 'egrave': 556, 'zacute': 500, 'iogonek': 222, 'Oacute': 778, 'oacute': 556, 'amacron': 556, 'sacute': 500, 'idieresis': 278, 'Ocircumflex': 778, 'Ugrave': 722, 'Delta': 612, 'thorn': 556, 'Odieresis': 778, 'mu': 556, 'igrave': 278, 'ohungarumlaut': 556, 'Eogonek': 667, 'dcroat': 556, 'threequarters': 834, 'Scedilla': 667, 'lcaron': 299, 'Kcommaaccent': 667, 'Lacute': 556, 'trademark': 1000, 'edotaccent': 556, 'Igrave': 278, 'Imacron': 278, 'Lcaron': 556, 'onehalf': 834, 'lessequal': 549, 'ocircumflex': 556, 'ntilde': 556, 'Uhungarumlaut': 722, 'Eacute': 667, 'emacron': 556, 'gbreve': 556, 'onequarter': 834, 'Scaron': 667, 'Scommaaccent': 667, 'Ohungarumlaut': 778, 'degree': 400, 'ograve': 556, 'Ccaron': 722, 'ugrave': 556, 'radical': 453, 'Dcaron': 722, 'rcommaaccent': 333, 'Ntilde': 722, 'otilde': 556, 'Rcommaaccent': 722, 'Lcommaaccent': 556, 'Atilde': 667, 'Aogonek': 667, 'Aring': 667, 'Otilde': 778, 'zdotaccent': 500, 'Ecaron': 667, 'Iogonek': 278, 'kcommaaccent': 500, 'minus': 584, 'Icircumflex': 278, 'ncaron': 556, 'tcommaaccent': 278, 'logicalnot': 584, 'odieresis': 556, 'udieresis': 556, 'notequal': 549, 'gcommaaccent': 556, 'eth': 556, 'zcaron': 500, 'ncommaaccent': 556, 'imacron': 278, 'Euro': 556} # type: ignore[annotation-unchecked]
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
