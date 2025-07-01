#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the Times Bold typeface and its properties.

The Times Bold typeface is a widely used serif font known for its readability
and emphasis. This class is typically used to render bold text in PDF documents
where the Times font is required.

It provides access to font-specific properties such as width, height, and character
mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class TimesBold(StandardType1Font):
    """
    Represents the Times Bold typeface and its properties.

    The Times Bold typeface is a widely used serif font known for its readability
    and emphasis. This class is typically used to render bold text in PDF documents
    where the Times font is required.

    It provides access to font-specific properties such as width, height, and character
    mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Times Bold font object with its specific attributes.

        The `TimesBold` class represents the Times Bold font, a Type1 font that applies bold styling to the Times font.
        This constructor sets the font's base attributes, including its encoding, font type,
        and width for various Unicode characters.
        The bold emphasis enhances visibility, making it ideal for headings and important sections in printed material.
        """
        super().__init__()
        self["BaseFont"] = name("Times-Bold")
        self["Encoding"] = name("WinAnsiEncoding")
        self["Subtype"] = name("Type1")
        self["Type"] = name("Font")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 250, 'exclam': 333, 'quotedbl': 555, 'numbersign': 500, 'dollar': 500, 'percent': 1000, 'ampersand': 833, 'quotesingle': 278, 'parenleft': 333, 'parenright': 333, 'asterisk': 500, 'plus': 570, 'comma': 250, 'hyphen': 333, 'period': 250, 'slash': 278, 'zero': 500, 'one': 500, 'two': 500, 'three': 500, 'four': 500, 'five': 500, 'six': 500, 'seven': 500, 'eight': 500, 'nine': 500, 'colon': 333, 'semicolon': 333, 'less': 570, 'equal': 570, 'greater': 570, 'question': 500, 'at': 930, 'A': 722, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 778, 'I': 389, 'J': 500, 'K': 778, 'L': 667, 'M': 944, 'N': 722, 'O': 778, 'P': 611, 'Q': 778, 'R': 722, 'S': 556, 'T': 667, 'U': 722, 'V': 722, 'W': 1000, 'X': 722, 'Y': 722, 'Z': 667, 'bracketleft': 333, 'backslash': 278, 'bracketright': 333, 'asciicircum': 581, 'underscore': 500, 'grave': 333, 'a': 500, 'b': 556, 'c': 444, 'd': 556, 'e': 444, 'f': 333, 'g': 500, 'h': 556, 'i': 278, 'j': 333, 'k': 556, 'l': 278, 'm': 833, 'n': 556, 'o': 500, 'p': 556, 'q': 556, 'r': 444, 's': 389, 't': 333, 'u': 556, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 444, 'braceleft': 394, 'bar': 220, 'braceright': 394, 'asciitilde': 520, 'exclamdown': 333, 'cent': 500, 'sterling': 500, 'currency': 500, 'yen': 500, 'brokenbar': 220, 'section': 500, 'dieresis': 333, 'copyright': 747, 'ordfeminine': 300, 'guillemetleft': 500, 'logicalnot': 570, 'registered': 747, 'macron': 333, 'degree': 400, 'plusminus': 570, 'acute': 333, 'paragraph': 540, 'periodcentered': 250, 'cedilla': 333, 'ordmasculine': 330, 'guillemetright': 500, 'onequarter': 750, 'onehalf': 750, 'threequarters': 750, 'questiondown': 500, 'Agrave': 722, 'Aacute': 722, 'Acircumflex': 722, 'Atilde': 722, 'Adieresis': 722, 'Aring': 722, 'AE': 1000, 'Ccedilla': 722, 'Egrave': 667, 'Eacute': 667, 'Ecircumflex': 667, 'Edieresis': 667, 'Igrave': 389, 'Iacute': 389, 'Icircumflex': 389, 'Idieresis': 389, 'Eth': 722, 'Ntilde': 722, 'Ograve': 778, 'Oacute': 778, 'Ocircumflex': 778, 'Otilde': 778, 'Odieresis': 778, 'multiply': 570, 'Oslash': 778, 'Ugrave': 722, 'Uacute': 722, 'Ucircumflex': 722, 'Udieresis': 722, 'Yacute': 722, 'Thorn': 611, 'germandbls': 556, 'agrave': 500, 'aacute': 500, 'acircumflex': 500, 'atilde': 500, 'adieresis': 500, 'aring': 500, 'ae': 722, 'ccedilla': 444, 'egrave': 444, 'eacute': 444, 'ecircumflex': 444, 'edieresis': 444, 'igrave': 278, 'iacute': 278, 'icircumflex': 278, 'idieresis': 278, 'eth': 500, 'ntilde': 556, 'ograve': 500, 'oacute': 500, 'ocircumflex': 500, 'otilde': 500, 'odieresis': 500, 'divide': 570, 'oslash': 500, 'ugrave': 556, 'uacute': 556, 'ucircumflex': 556, 'udieresis': 556, 'yacute': 500, 'thorn': 556, 'ydieresis': 500, 'Amacron': 722, 'amacron': 500, 'Abreve': 722, 'abreve': 500, 'Aogonek': 722, 'aogonek': 500, 'Cacute': 722, 'cacute': 444, 'Ccaron': 722, 'ccaron': 444, 'Dcaron': 722, 'dcaron': 672, 'Dcroat': 722, 'dcroat': 556, 'Emacron': 667, 'emacron': 444, 'Edotaccent': 667, 'edotaccent': 444, 'Eogonek': 667, 'eogonek': 444, 'Ecaron': 667, 'ecaron': 444, 'Gbreve': 778, 'gbreve': 500, 'Gcommaaccent': 778, 'gcommaaccent': 500, 'Imacron': 389, 'imacron': 278, 'Iogonek': 389, 'iogonek': 278, 'Idotaccent': 389, 'dotlessi': 278, 'Kcommaaccent': 778, 'kcommaaccent': 556, 'Lacute': 667, 'lacute': 278, 'Lcommaaccent': 667, 'lcommaaccent': 278, 'Lcaron': 667, 'lcaron': 394, 'Lslash': 667, 'lslash': 278, 'Nacute': 722, 'nacute': 556, 'Ncommaaccent': 722, 'ncommaaccent': 556, 'Ncaron': 722, 'ncaron': 556, 'Omacron': 778, 'omacron': 500, 'Ohungarumlaut': 778, 'ohungarumlaut': 500, 'OE': 1000, 'oe': 722, 'Racute': 722, 'racute': 444, 'Rcommaaccent': 722, 'rcommaaccent': 444, 'Rcaron': 722, 'rcaron': 444, 'Sacute': 556, 'sacute': 389, 'Scedilla': 556, 'scedilla': 389, 'Scaron': 556, 'scaron': 389, 'Tcaron': 667, 'tcaron': 416, 'Umacron': 722, 'umacron': 556, 'Uring': 722, 'uring': 556, 'Uhungarumlaut': 722, 'uhungarumlaut': 556, 'Uogonek': 722, 'uogonek': 556, 'Ydieresis': 722, 'Zacute': 667, 'zacute': 444, 'Zdotaccent': 667, 'zdotaccent': 444, 'Zcaron': 667, 'zcaron': 444, 'Scommaaccent': 556, 'scommaaccent': 389, 'Tcommaaccent': 667, 'tcommaaccent': 333, 'circumflex': 333, 'caron': 333, 'breve': 333, 'dotaccent': 333, 'ring': 333, 'ogonek': 333, 'tilde': 333, 'hungarumlaut': 333, 'Delta': 612, 'mu': 556, 'endash': 500, 'emdash': 1000, 'quoteleft': 333, 'quoteright': 333, 'quotesinglbase': 333, 'quotedblleft': 500, 'quotedblright': 500, 'quotedblbase': 500, 'dagger': 500, 'daggerdbl': 500, 'bullet': 350, 'ellipsis': 1000, 'perthousand': 1000, 'guilsinglleft': 333, 'guilsinglright': 333, 'fraction': 167, 'Euro': 500, 'trademark': 1000, 'partialdiff': 494, 'summation': 600, 'minus': 570, 'radical': 549, 'notequal': 549, 'lessequal': 549, 'greaterequal': 549, 'lozenge': 494, 'fi': 556, 'fl': 556} # type: ignore[annotation-unchecked]
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
