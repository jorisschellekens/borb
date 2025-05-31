#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a color in the CMYK (Cyan, Magenta, Yellow, Black) color model.

The CMYK color model, also known as process color, is used in color printing and describes the printing
process itself. CMYK refers to the four ink plates used in color printing: cyan, magenta, yellow, and key (black).

The model works by masking colors on a lighter, typically white, background. The ink reduces the light
that would otherwise be reflected, and this subtractive model "subtracts" red, green, and blue from white light.
White light minus red leaves cyan, minus green leaves magenta, and minus blue leaves yellow.

In contrast to additive models like RGB, where white is a combination of all primary lights and black is
the absence of light, CMYK works oppositely. White is the paper's natural color, while black results
from combining all inks. To achieve deeper black tones and reduce ink usage, black ink is often used
instead of a combination of cyan, magenta, and yellow.
"""
from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor


class CMYKColor(Color):
    """
    Represents a color in the CMYK (Cyan, Magenta, Yellow, Black) color model.

    The CMYK color model, also known as process color, is used in color printing and describes the printing
    process itself. CMYK refers to the four ink plates used in color printing: cyan, magenta, yellow, and key (black).

    The model works by masking colors on a lighter, typically white, background. The ink reduces the light
    that would otherwise be reflected, and this subtractive model "subtracts" red, green, and blue from white light.
    White light minus red leaves cyan, minus green leaves magenta, and minus blue leaves yellow.

    In contrast to additive models like RGB, where white is a combination of all primary lights and black is
    the absence of light, CMYK works oppositely. White is the paper's natural color, while black results
    from combining all inks. To achieve deeper black tones and reduce ink usage, black ink is often used
    instead of a combination of cyan, magenta, and yellow.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, cyan: float, magenta: float, yellow: float, key: float):
        """
        Initialize a CMYKColor object with specified cyan, magenta, yellow, and key (black) values.

        The `CMYKColor` class represents a color using the CMYK (Cyan, Magenta, Yellow, Key/Black) model,
        commonly used in color printing.
        Each component (cyan, magenta, yellow, key) is a float in the range of 0 to 1,
        representing the intensity of each color.

        :param cyan:    The intensity of the cyan component, must be between 0 and 1.
        :param magenta: The intensity of the magenta component, must be between 0 and 1.
        :param yellow:  The intensity of the yellow component, must be between 0 and 1.
        :param key:     The intensity of the key (black) component, must be between 0 and 1.
        """
        super().__init__()
        # fmt: off
        assert 0 <= cyan <= 1, f"Cyan component out of range: {cyan}. Must be between 0 and 1."
        assert 0 <= key <= 1, f"Key component out of range: {key}. Must be between 0 and 1."
        assert 0 <= magenta <= 1, f"Magenta component out of range: {magenta}. Must be between 0 and 1."
        assert 0 <= yellow <= 1, f"Yellow component out of range: {yellow}. Must be between 0 and 1."
        # fmt: on
        self.__cyan: float = cyan
        self.__key: float = key
        self.__magenta: float = magenta
        self.__yellow: float = yellow

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_cyan(self) -> float:
        """
        Retrieve the cyan component of the CMYK color.

        This method returns the cyan component as a float in the range [0, 1].

        :return: The cyan component of this CMYKColor, as a float between 0 and 1.
        """
        return self.__cyan

    def get_key(self) -> float:
        """
        Retrieve the key component of the CMYK color.

        This method returns the key component as a float in the range [0, 1].

        :return: The key component of this CMYKColor, as a float between 0 and 1.
        """
        return self.__key

    def get_magenta(self) -> float:
        """
        Retrieve the magenta component of the CMYK color.

        This method returns the magenta component as a float in the range [0, 1].

        :return: The magenta component of this CMYKColor, as a float between 0 and 1.
        """
        return self.__magenta

    def get_yellow(self) -> float:
        """
        Retrieve the yellow component of the CMYK color.

        This method returns the yellow component as a float in the range [0, 1].

        :return: The yellow component of this CMYKColor, as a float between 0 and 1.
        """
        return self.__yellow

    def to_rgb_color(self) -> RGBColor:
        """
        Convert the current color representation to RGB format.

        This method transforms the current color into an equivalent RGB (Red, Green, Blue)
        representation. It returns a new RGBColor object containing the RGB components of
        the current color.

        :return: A new RGBColor object representing the current color in RGB format.
        """
        return RGBColor(
            red=int(255 * (1.0 - self.__cyan) * (1.0 - self.__key)),
            green=int(255 * (1.0 - self.__magenta) * (1.0 - self.__key)),
            blue=int(255 * (1.0 - self.__yellow) * (1.0 - self.__key)),
        )
