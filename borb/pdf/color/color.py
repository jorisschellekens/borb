#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the characteristic of visual perception described through color categories like red, green, and blue.

Color perception is derived from the stimulation of photoreceptor cells, particularly cone cells in the human eye,
by electromagnetic radiation in the visible spectrum. The color associated with an object is influenced by the
wavelengths of light reflected from the object and its intensity, determined by the object's physical properties
such as absorption and emission spectra.
"""


class Color(dict):
    """
    Represents the characteristic of visual perception described through color categories like red, green, and blue.

    Color perception is derived from the stimulation of photoreceptor cells, particularly cone cells in the human eye,
    by electromagnetic radiation in the visible spectrum. The color associated with an object is influenced by the
    wavelengths of light reflected from the object and its intensity, determined by the object's physical properties
    such as absorption and emission spectra.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def darker(self) -> "Color":
        """
        Create a darker version of the current color.

        This method reduces the brightness of the current color by a specified factor,
        resulting in a new color object that is a darker shade. The original color remains
        unchanged.

        :return:    a new Color object that is a darker shade of the current color.
        """
        from borb.pdf.color.rgb_color import RGBColor

        c1: RGBColor = self.to_rgb_color()
        c2: RGBColor = RGBColor(0, 0, 0)
        alpha: float = 0.05
        r: int = min(int(c1.get_red() * (1.0 - alpha) + c2.get_red() * alpha), 255)
        g: int = min(int(c1.get_green() * (1.0 - alpha) + c2.get_green() * alpha), 255)
        b: int = min(int(c1.get_blue() * (1.0 - alpha) + c2.get_blue() * alpha), 255)
        return RGBColor(r, g, b)

    def lighter(self) -> "Color":
        """
        Create a lighter version of the current color.

        This method enhances the brightness of the current color by a specified factor,
        resulting in a new color object that is a lighter shade. The original color remains
        unchanged.

        :return:    a new Color object that is a lighter shade of the current color.
        """
        from borb.pdf.color.rgb_color import RGBColor

        c1: RGBColor = self.to_rgb_color()
        c2: RGBColor = RGBColor(255, 255, 255)
        alpha: float = 0.05
        r: int = min(int(c1.get_red() * (1.0 - alpha) + c2.get_red() * alpha), 255)
        g: int = min(int(c1.get_green() * (1.0 - alpha) + c2.get_green() * alpha), 255)
        b: int = min(int(c1.get_blue() * (1.0 - alpha) + c2.get_blue() * alpha), 255)
        return RGBColor(r, g, b)

    def to_rgb_color(self) -> "RGBColor":  # type: ignore[name-defined]
        """
        Convert the current color representation to RGB format.

        This method transforms the current color into an equivalent RGB (Red, Green, Blue)
        representation. It returns a new RGBColor object containing the RGB components of
        the current color.

        :return: A new RGBColor object representing the current color in RGB format.
        """
        return None
