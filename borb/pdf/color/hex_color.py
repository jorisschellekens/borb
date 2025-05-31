#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a color defined by a hexadecimal triplet.

A hex triplet is a six-digit, three-byte hexadecimal number used in HTML, CSS,
SVG, and other applications to represent colors. The three bytes correspond to
the red, green, and blue components of the color, with each byte ranging from
00 to FF in hexadecimal (or 0 to 255 in decimal), indicating the intensity of
each color component.

This representation follows the 24-bit RGB color scheme, where:
- Byte 1: Red value
- Byte 2: Green value
- Byte 3: Blue value

Hex triplets are commonly used in web design to specify colors.
"""
from borb.pdf.color.rgb_color import RGBColor


class HexColor(RGBColor):
    """
    Represents a color defined by a hexadecimal triplet.

    A hex triplet is a six-digit, three-byte hexadecimal number used in HTML, CSS,
    SVG, and other applications to represent colors. The three bytes correspond to
    the red, green, and blue components of the color, with each byte ranging from
    00 to FF in hexadecimal (or 0 to 255 in decimal), indicating the intensity of
    each color component.

    This representation follows the 24-bit RGB color scheme, where:
    - Byte 1: Red value
    - Byte 2: Green value
    - Byte 3: Blue value

    Hex triplets are commonly used in web design to specify colors.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, hex: str):
        """
        Initialize a HexColor object using a hexadecimal color code.

        The `HexColor` class represents a color defined by a hexadecimal string, such as "#FF5733" or "FF5733".
        This constructor parses the provided hex string, validates it,
        and converts it into its corresponding RGB components.
        It also supports shorthand hex codes (e.g., "#F00" is expanded to "#FF0000").

        :param hex: A string representing the hex color code, with or without a leading '#'.
                    It should be either a 3-character shorthand (e.g., "#F00")
                    or a 6-character full form (e.g., "#FF5733").
        """
        # trim leading # if needed
        if hex.startswith("#"):
            hex = hex[1:]

        # convert to uppercase
        hex = hex.upper()

        # shorthand css
        if len(hex) == 3:
            hex = "".join([char * 2 for char in hex])

        # fmt: off
        assert len(hex) == 6, f"Hex color code must be 6 characters long after processing, got: '{hex}'."
        assert all([c in "0123456789ABCDEF" for c in hex]), f"Invalid hex color code '{hex}'. Must contain only hexadecimal digits (0-9, A-F)."
        # fmt: on

        # call to super
        r, g, b = int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)
        super().__init__(red=r, green=g, blue=b)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
