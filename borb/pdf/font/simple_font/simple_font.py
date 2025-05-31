#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a simple font and its properties in a PDF document.

The `SimpleFont` class encapsulates the basic characteristics of a font used in PDF
documents. It provides common properties and methods for working with fonts, such as
character mappings, font metrics, and rendering capabilities. This class serves as the
foundation for more specialized font classes (e.g., `Type1Font`), offering basic font
functionality while allowing for more specific implementations. Simple fonts are used
in a variety of contexts, from basic text rendering to complex document layouts.
"""
import typing

from borb.pdf.font.font import Font
from borb.pdf.primitives import name


class SimpleFont(Font):
    """
    Represents a simple font and its properties in a PDF document.

    The `SimpleFont` class encapsulates the basic characteristics of a font used in PDF
    documents. It provides common properties and methods for working with fonts, such as
    character mappings, font metrics, and rendering capabilities. This class serves as the
    foundation for more specialized font classes (e.g., `Type1Font`), offering basic font
    functionality while allowing for more specific implementations. Simple fonts are used
    in a variety of contexts, from basic text rendering to complex document layouts.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a SimpleFont instance.

        The `SimpleFont` class represents a base class for simple fonts in a PDF. Simple fonts
        use a single-byte encoding for character codes, with support for character mapping through
        encodings, differences, or CMaps.

        This constructor initializes the font with default properties, allowing it to be customized
        or extended to represent specific font types.
        """
        super().__init__()

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_encoding_or_base_encoding(self) -> name:
        """
        Retrieve the encoding or base encoding of the Simple Font.

        This method determines the encoding used by the font, prioritizing the following cases:
        1. If `/Encoding` is a dictionary and contains a `/BaseEncoding` key, the value of `/BaseEncoding`
           (a `name` object) is returned.
        2. If `/Encoding` is directly a `name` object, it is returned as the font's encoding.
        3. If neither of the above is present, the method defaults to `StandardEncoding`, which is the
           common default for simple fonts.

        This logic ensures that the correct encoding is used, whether explicitly defined or falling back
        to a standard default.

        :return: The encoding or base encoding of the font as a `name` object.
        """
        # /Encoding /BaseEncoding
        if (
            "Encoding" in self
            and isinstance(self["Encoding"], dict)
            and "BaseEncoding" in self["Encoding"]
            and isinstance(self["Encoding"]["BaseEncoding"], name)
        ):
            return self["Encoding"]["BaseEncoding"]

        # /Encoding
        if "Encoding" in self and isinstance(self["Encoding"], name):
            return self["Encoding"]

        # return
        return name("StandardEncoding")

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
        # first char
        first_char: int = self.get("FirstChar", 0)

        # last char
        last_char: int = self.get("LastChar", 255)

        # widths
        widths: typing.List[int] = self.get("Widths", [])

        # missing_width
        missing_width: int = self.get("FontDescriptor", {}).get("MissingWidth", 0)

        # look up individual character codes
        # fmt: off
        character_codes: typing.List[int] = [self.get_character_code(c) for c in text]
        # fmt: on

        # look up character width
        character_width: typing.List[float] = [
            (widths[c - first_char] if first_char <= c <= last_char else missing_width)
            for c in character_codes
        ]
        character_width = [w / 1000 for w in character_width]

        # apply character spacing
        character_width = [(w + character_spacing) for w in character_width]
        character_width[-1] -= character_spacing

        # apply word spacing
        character_width = [
            (w + word_spacing) if text[i] == " " else w
            for i, w in enumerate(character_width)
        ]

        # apply font size
        import math

        return math.ceil(sum(character_width) * font_size)
