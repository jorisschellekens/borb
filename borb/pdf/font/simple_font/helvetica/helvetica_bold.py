#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the Helvetica Bold typeface and its properties.

The Helvetica Bold typeface is a widely used sans-serif font known for its
clean and modern appearance. This class is typically used to render text in
PDF documents where Helvetica Bold is required.

It provides access to font-specific properties such as width, height, and
character mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class HelveticaBold(StandardType1Font):
    """
    Represents the Helvetica Bold typeface and its properties.

    The Helvetica Bold typeface is a widely used sans-serif font known for its
    clean and modern appearance. This class is typically used to render text in
    PDF documents where Helvetica Bold is required.

    It provides access to font-specific properties such as width, height, and
    character mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Helvetica-Bold font object with its specific attributes.

        The `HelveticaBold` class represents the Helvetica-Bold font,
        a Type1 font that applies bold styling to the Helvetica font.
        This constructor sets the font's base attributes, including its encoding, font type,
        and width for various Unicode characters.
        The font uses proportional spacing while providing bold emphasis,
        making it ideal for headings and emphasized text.
        """
        super().__init__()
        self["BaseFont"] = name("Helvetica-Bold")
        self["Encoding"] = name("WinAnsiEncoding")
        self["Subtype"] = name("Type1")
        self["Type"] = name("Font")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 278, 'exclam': 333, 'quotedbl': 474, 'numbersign': 556, 'dollar': 556, 'percent': 889, 'ampersand': 722, 'quotesingle': 238, 'quoteright': 278, 'parenleft': 333, 'parenright': 333, 'asterisk': 389, 'plus': 584, 'comma': 278, 'hyphen': 333, 'period': 278, 'slash': 278, 'zero': 556, 'one': 556, 'two': 556, 'three': 556, 'four': 556, 'five': 556, 'six': 556, 'seven': 556, 'eight': 556, 'nine': 556, 'colon': 333, 'semicolon': 333, 'less': 584, 'equal': 584, 'greater': 584, 'question': 611, 'at': 975, 'A': 722, 'B': 722, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 722, 'I': 278, 'J': 556, 'K': 722, 'L': 611, 'M': 833, 'N': 722, 'O': 778, 'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944, 'X': 667, 'Y': 667, 'Z': 611, 'bracketleft': 333, 'backslash': 278, 'bracketright': 333, 'asciicircum': 584, 'underscore': 556, 'grave': 333, 'quoteleft': 278, 'a': 556, 'b': 611, 'c': 556, 'd': 611, 'e': 556, 'f': 333, 'g': 611, 'h': 611, 'i': 278, 'j': 278, 'k': 556, 'l': 278, 'm': 889, 'n': 611, 'o': 611, 'p': 611, 'q': 611, 'r': 389, 's': 556, 't': 333, 'u': 611, 'v': 556, 'w': 778, 'x': 556, 'y': 556, 'z': 500, 'braceleft': 389, 'bar': 280, 'braceright': 389, 'asciitilde': 584, 'exclamdown': 333, 'cent': 556, 'sterling': 556, 'fraction': 167, 'yen': 556, 'brokenbar': 280, 'section': 556, 'currency': 556, 'quotedblleft': 500, 'guillemetleft': 556, 'guilsinglleft': 333, 'guilsinglright': 333, 'fi': 611, 'fl': 611, 'endash': 556, 'dagger': 556, 'daggerdbl': 556, 'periodcentered': 278, 'paragraph': 556, 'bullet': 350, 'quotesinglbase': 278, 'quotedblbase': 500, 'quotedblright': 500, 'guillemetright': 556, 'ellipsis': 1000, 'perthousand': 1000, 'questiondown': 611, 'acute': 333, 'circumflex': 333, 'tilde': 333, 'macron': 333, 'breve': 333, 'dotaccent': 333, 'dieresis': 333, 'ring': 333, 'cedilla': 333, 'hungarumlaut': 333, 'ogonek': 333, 'caron': 333, 'emdash': 1000, 'AE': 1000, 'ordfeminine': 370, 'Lslash': 611, 'Oslash': 778, 'OE': 1000, 'ordmasculine': 365, 'ae': 889, 'dotlessi': 278, 'lslash': 278, 'oslash': 611, 'oe': 944, 'germandbls': 611, 'Idieresis': 278, 'eacute': 556, 'abreve': 556, 'uhungarumlaut': 611, 'ecaron': 556, 'Ydieresis': 667, 'divide': 584, 'Yacute': 667, 'Acircumflex': 722, 'aacute': 556, 'Ucircumflex': 722, 'yacute': 556, 'scommaaccent': 556, 'ecircumflex': 556, 'Uring': 722, 'Udieresis': 722, 'aogonek': 556, 'Uacute': 722, 'uogonek': 611, 'Edieresis': 667, 'Dcroat': 722, 'copyright': 737, 'Emacron': 667, 'ccaron': 556, 'aring': 556, 'Ncommaaccent': 722, 'lacute': 278, 'agrave': 556, 'Tcommaaccent': 611, 'Cacute': 722, 'atilde': 556, 'Edotaccent': 667, 'scaron': 556, 'scedilla': 556, 'iacute': 278, 'lozenge': 494, 'Rcaron': 722, 'Gcommaaccent': 778, 'ucircumflex': 611, 'acircumflex': 556, 'Amacron': 722, 'rcaron': 389, 'ccedilla': 556, 'Zdotaccent': 611, 'Thorn': 667, 'Omacron': 778, 'Racute': 722, 'Sacute': 667, 'dcaron': 743, 'Umacron': 722, 'uring': 611, 'Ograve': 778, 'Agrave': 722, 'Abreve': 722, 'multiply': 584, 'uacute': 611, 'Tcaron': 611, 'partialdiff': 494, 'ydieresis': 556, 'Nacute': 722, 'icircumflex': 278, 'Ecircumflex': 667, 'adieresis': 556, 'edieresis': 556, 'cacute': 556, 'nacute': 611, 'umacron': 611, 'Ncaron': 722, 'Iacute': 278, 'plusminus': 584, 'registered': 737, 'Gbreve': 778, 'Idotaccent': 278, 'summation': 600, 'Egrave': 667, 'racute': 389, 'omacron': 611, 'Zacute': 611, 'Zcaron': 611, 'greaterequal': 549, 'Eth': 722, 'Ccedilla': 722, 'lcommaaccent': 278, 'tcaron': 389, 'eogonek': 556, 'Uogonek': 722, 'Aacute': 722, 'Adieresis': 722, 'egrave': 556, 'zacute': 500, 'iogonek': 278, 'Oacute': 778, 'oacute': 611, 'amacron': 556, 'sacute': 556, 'idieresis': 278, 'Ocircumflex': 778, 'Ugrave': 722, 'Delta': 612, 'thorn': 611, 'Odieresis': 778, 'mu': 611, 'igrave': 278, 'ohungarumlaut': 611, 'Eogonek': 667, 'dcroat': 611, 'threequarters': 834, 'Scedilla': 667, 'lcaron': 400, 'Kcommaaccent': 722, 'Lacute': 611, 'trademark': 1000, 'edotaccent': 556, 'Igrave': 278, 'Imacron': 278, 'Lcaron': 611, 'onehalf': 834, 'lessequal': 549, 'ocircumflex': 611, 'ntilde': 611, 'Uhungarumlaut': 722, 'Eacute': 667, 'emacron': 556, 'gbreve': 611, 'onequarter': 834, 'Scaron': 667, 'Scommaaccent': 667, 'Ohungarumlaut': 778, 'degree': 400, 'ograve': 611, 'Ccaron': 722, 'ugrave': 611, 'radical': 549, 'Dcaron': 722, 'rcommaaccent': 389, 'Ntilde': 722, 'otilde': 611, 'Rcommaaccent': 722, 'Lcommaaccent': 611, 'Atilde': 722, 'Aogonek': 722, 'Aring': 722, 'Otilde': 778, 'zdotaccent': 500, 'Ecaron': 667, 'Iogonek': 278, 'kcommaaccent': 556, 'minus': 584, 'Icircumflex': 278, 'ncaron': 611, 'tcommaaccent': 333, 'logicalnot': 584, 'odieresis': 611, 'udieresis': 611, 'notequal': 549, 'gcommaaccent': 611, 'eth': 611, 'zcaron': 500, 'ncommaaccent': 611, 'imacron': 278, 'Euro': 556} # type: ignore[annotation-unchecked]
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
