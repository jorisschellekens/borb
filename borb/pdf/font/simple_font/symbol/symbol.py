#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the Symbol typeface and its properties.

The Symbol typeface is a widely used symbol font that provides a collection of
special characters and symbols. This class is typically used to render text in PDF
documents where the Symbol font is required.

It provides access to font-specific properties such as width, height, and character
mapping.
"""
import typing

from borb.pdf.font.adobe_glyph_list import AdobeGlyphList
from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font
from borb.pdf.primitives import name


class Symbol(StandardType1Font):
    """
    Represents the Symbol typeface and its properties.

    The Symbol typeface is a widely used symbol font that provides a collection of
    special characters and symbols. This class is typically used to render text in PDF
    documents where the Symbol font is required.

    It provides access to font-specific properties such as width, height, and character
    mapping.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a Symbol font representation.

        The `Symbol` class is used to represent the Symbol font in a document.
        It initializes various attributes associated with the font, including type, subtype, base font name,
        and encoding.
        Additionally, it sets up mappings for character IDs to Unicode values and their respective widths.
        """
        super().__init__()
        self["Type"] = name("Font")
        self["Subtype"] = name("Type1")
        self["BaseFont"] = name("Symbol")
        self["Encoding"] = name("Symbol")
        # fmt: off
        self.__character_name_to_width: typing.Dict[str, int] = {'space': 250, 'exclam': 333, 'universal': 713, 'numbersign': 500, 'existential': 549, 'percent': 833, 'ampersand': 778, 'suchthat': 439, 'parenleft': 333, 'parenright': 333, 'asteriskmath': 500, 'plus': 549, 'comma': 250, 'minus': 549, 'period': 250, 'slash': 278, 'zero': 500, 'one': 500, 'two': 500, 'three': 500, 'four': 500, 'five': 500, 'six': 500, 'seven': 500, 'eight': 500, 'nine': 500, 'colon': 278, 'semicolon': 278, 'less': 549, 'equal': 549, 'greater': 549, 'question': 444, 'congruent': 549, 'Alpha': 722, 'Beta': 667, 'Chi': 722, 'Delta': 612, 'Epsilon': 611, 'Phi': 763, 'Gamma': 603, 'Eta': 722, 'Iota': 333, 'J': 631, 'Kappa': 722, 'Lambda': 686, 'Mu': 889, 'Nu': 722, 'Omicron': 722, 'Pi': 768, 'Theta': 741, 'Rho': 556, 'Sigma': 592, 'Tau': 611, 'Upsilon': 690, 'V': 439, 'Omega': 768, 'Xi': 645, 'Psi': 795, 'Zeta': 611, 'bracketleft': 333, 'therefore': 863, 'bracketright': 333, 'perpendicular': 658, 'underscore': 500, 'grave': 500, 'alpha': 631, 'beta': 549, 'chi': 549, 'delta': 494, 'epsilon': 439, 'phi': 521, 'gamma': 411, 'eta': 603, 'iota': 329, 'j': 603, 'kappa': 549, 'lambda': 549, 'mu': 576, 'nu': 521, 'omicron': 549, 'pi': 549, 'theta': 521, 'rho': 549, 'sigma': 603, 'tau': 439, 'upsilon': 576, 'v': 713, 'omega': 686, 'xi': 493, 'psi': 686, 'zeta': 494, 'braceleft': 480, 'bar': 200, 'braceright': 480, 'similar': 549, 'Euro': 750, 'exclamdown': 620, 'minute': 247, 'lessequal': 549, 'fraction': 167, 'infinity': 713, 'brokenbar': 500, 'section': 753, 'dieresis': 753, 'copyright': 753, 'ordfeminine': 753, 'guillemetleft': 1042, 'arrowleft': 987, 'arrowup': 603, 'arrowright': 987, 'arrowdown': 603, 'degree': 400, 'plusminus': 549, 'second': 411, 'greaterequal': 549, 'multiply': 549, 'proportional': 713, 'partialdiff': 494, 'bullet': 460, 'divide': 384, 'notequal': 549, 'equivalence': 549, 'approxequal': 549, 'ellipsis': 1000, 'onehalf': 603, 'threequarters': 1000, 'questiondown': 658, 'aleph': 823, 'Ifraktur': 686, 'Rfraktur': 795, 'weierstrass': 987, 'circlemultiply': 768, 'circleplus': 768, 'emptyset': 823, 'intersection': 768, 'union': 768, 'propersuperset': 713, 'reflexsuperset': 713, 'notsubset': 713, 'propersubset': 713, 'reflexsubset': 713, 'element': 713, 'notelement': 713, 'angle': 768, 'gradient': 713, 'Ograve': 790, 'Oacute': 790, 'Ocircumflex': 890, 'product': 823, 'radical': 549, 'dotmath': 250, 'logicalnot': 713, 'logicaland': 603, 'logicalor': 603, 'Ucircumflex': 1042, 'Udieresis': 987, 'Yacute': 603, 'Thorn': 987, 'germandbls': 603, 'lozenge': 494, 'angleleft': 329, 'acircumflex': 790, 'atilde': 790, 'adieresis': 786, 'summation': 713, 'ae': 384, 'ccedilla': 384, 'egrave': 384, 'eacute': 384, 'ecircumflex': 384, 'edieresis': 384, 'igrave': 494, 'iacute': 494, 'icircumflex': 494, 'idieresis': 494, 'angleright': 329, 'integral': 274, 'integraltp': 686, 'ocircumflex': 686, 'integralbt': 686, 'odieresis': 384, 'oslash': 384, 'ugrave': 384, 'uacute': 384, 'ucircumflex': 384, 'udieresis': 494, 'yacute': 494, 'thorn': 494} # type: ignore[annotation-unchecked]
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
