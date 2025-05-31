#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an RGB color space based on the additive RGB color model.

This class defines a color space that employs RGB primaries, characterized by
the chromaticities of red, green, and blue. It can produce any color within the
2D triangle formed by these primary colors (excluding factors like transfer function
and white point).

The primary colors are specified using their CIE 1931 color space chromaticity
coordinates (x, y), linking them to human-visible colors.

RGB stands for red, green, and blue.
"""
from borb.pdf.color.color import Color


class RGBColor(Color):
    """
    Represents an RGB color space based on the additive RGB color model.

    This class defines a color space that employs RGB primaries, characterized by
    the chromaticities of red, green, and blue. It can produce any color within the
    2D triangle formed by these primary colors (excluding factors like transfer function
    and white point).

    The primary colors are specified using their CIE 1931 color space chromaticity
    coordinates (x, y), linking them to human-visible colors.

    RGB stands for red, green, and blue.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        """
        Initialize an RGBColor object with specified red, green, and blue values.

        The `RGBColor` class represents a color using the RGB (Red, Green, Blue) model,
        where each component (red, green, blue) is an integer ranging from 0 to 255.
        The color is defined by these three values, which control the intensity of each component.

        :param red:     The intensity of the red component, default is 0. Must be between 0 and 255.
        :param green:   The intensity of the green component, default is 0. Must be between 0 and 255.
        :param blue:    The intensity of the blue component, default is 0. Must be between 0 and 255.
        """
        super().__init__()
        # fmt: off
        assert 0 <= blue <= 255, f"Blue component out of range: {blue}. Must be between 0 and 255."
        assert 0 <= green <= 255, f"Green component out of range: {green}. Must be between 0 and 255."
        assert 0 <= red <= 255, f"Red component out of range: {red}. Must be between 0 and 255."
        # fmt: on
        self.__blue: int = blue
        self.__green: int = green
        self.__red: int = red

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_blue(self) -> int:
        """
        Retrieve the blue component of the RGB color.

        This method returns the blue component as an integer in the range [0, 255].

        :return: The blue component of this RGBColor, as an integer between 0 and 255.
        """
        return self.__blue

    def get_green(self) -> int:
        """
        Retrieve the green component of the RGB color.

        This method returns the green component as an integer in the range [0, 255].

        :return: The green component of this RGBColor, as an integer between 0 and 255.
        """
        return self.__green

    def get_red(self) -> int:
        """
        Retrieve the red component of the RGB color.

        This method returns the red component as an integer in the range [0, 255].

        :return: The red component of this RGBColor, as an integer between 0 and 255.
        """
        return self.__red

    def to_hex_str(self) -> str:
        """
        Convert the RGB color to a hexadecimal string representation.

        This method converts the red, green, and blue components of the `RGBColor` instance
        into a hexadecimal string in the format `#RRGGBB`, where each component is represented
        by two uppercase hexadecimal digits.

        :return: A string representing the color in hexadecimal format.
        """
        return f"#{self.__red:02X}{self.__green:02X}{self.__blue:02X}"

    def to_hsv_color(self) -> "HSVColor":  # type: ignore[name-defined]
        """
        Convert the RGB color to an HSV color.

        This method converts the red, green, and blue components of the `RGBColor` instance
        into hue, saturation, and value components of the HSV color model.

        :return: A new HSVColor object representing the color in HSV format.
        """
        # Normalize RGB values to [0, 1]
        r: float = self.get_red() / 255.0
        g: float = self.get_green() / 255.0
        b: float = self.get_blue() / 255.0

        # Find min and max values among r, g, b
        max_val: float = max(r, g, b)
        min_val: float = min(r, g, b)
        delta: float = max_val - min_val

        # Calculate Hue (H)
        h: int = 0
        if delta == 0:
            h = 0
        elif max_val == r:
            h = int(60 * ((g - b) / delta) + 360) % 360
        elif max_val == g:
            h = int(60 * ((b - r) / delta) + 120) % 360
        else:
            h = int(60 * ((r - g) / delta) + 240) % 360

        # Calculate Saturation (S)
        s = 0 if max_val == 0 else delta / max_val

        # Calculate Value (V)
        v = max_val

        # Return HSVColor
        from borb.pdf.color.hsv_color import HSVColor

        return HSVColor(hue=h, saturation=s, value=v)

    def to_rgb_color(self) -> "RGBColor":
        """
        Convert the current color representation to RGB format.

        This method transforms the current color into an equivalent RGB (Red, Green, Blue)
        representation. It returns a new RGBColor object containing the RGB components of
        the current color.

        :return: A new RGBColor object representing the current color in RGB format.
        """
        return self
