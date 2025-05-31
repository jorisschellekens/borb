#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an HSV (Hue, Saturation, Value) color.

HSL (Hue, Saturation, Lightness) and HSV are alternative representations of the RGB color model,
developed in the 1970s by computer graphics researchers to better align with human color perception.
In these models, colors of each hue are arranged in a radial slice around a central axis of neutral
colors, ranging from black at the bottom to white at the top.

The HSL representation models how different paints mix in the real world, with the lightness dimension
resembling varying amounts of black or white paint in the mixture. For instance, to create "light red,"
a red pigment can be mixed with white paint, corresponding to a high "lightness" value. Fully saturated
colors are placed around a circle at a lightness value of ½, while lightness values of 0 and 1 correspond
to fully black and white, respectively.

The HSV representation, on the other hand, models how colors appear under light. The main difference
between HSL and HSV is that in HSL, maximum lightness results in pure white, while in HSV, maximum
value (brightness) simulates shining a bright white light on a colored object. For example, shining
bright white light on a red object makes it appear brighter and more intense, whereas shining a dim
light on the same object results in a darker appearance.
"""
import math

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor


class HSVColor(Color):
    """
    Represents an HSV (Hue, Saturation, Value) color.

    HSL (Hue, Saturation, Lightness) and HSV are alternative representations of the RGB color model,
    developed in the 1970s by computer graphics researchers to better align with human color perception.
    In these models, colors of each hue are arranged in a radial slice around a central axis of neutral
    colors, ranging from black at the bottom to white at the top.

    The HSL representation models how different paints mix in the real world, with the lightness dimension
    resembling varying amounts of black or white paint in the mixture. For instance, to create "light red,"
    a red pigment can be mixed with white paint, corresponding to a high "lightness" value. Fully saturated
    colors are placed around a circle at a lightness value of ½, while lightness values of 0 and 1 correspond
    to fully black and white, respectively.

    The HSV representation, on the other hand, models how colors appear under light. The main difference
    between HSL and HSV is that in HSL, maximum lightness results in pure white, while in HSV, maximum
    value (brightness) simulates shining a bright white light on a colored object. For example, shining
    bright white light on a red object makes it appear brighter and more intense, whereas shining a dim
    light on the same object results in a darker appearance.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, hue: float, saturation: float, value: float):
        """
        Initialize an HSVColor object with the given hue, saturation, and value components.

        The `HSVColor` class represents a color in the HSV (Hue, Saturation, Value) color model.
        This constructor initializes the color using the specified hue, saturation, and value, where:
        - `hue` represents the color's angle on the color wheel (0 to 360 degrees).
        - `saturation` defines the intensity of the color (0 for grayscale to 1 for full color).
        - `value` indicates the brightness of the color (0 for black to 1 for full brightness).

        :param hue: The hue of the color, in degrees (0 <= hue <= 360).
        :param saturation: The saturation level of the color (0 <= saturation <= 1).
        :param value: The brightness level of the color (0 <= value <= 1).
        """
        super().__init__()
        # fmt: off
        assert 0 <= hue <= 360, f"Hue out of range: {hue}. Must be between 0 and 360."
        assert 0 <= saturation <= 1, f"Saturation out of range: {saturation}. Must be between 0 and 1."
        assert 0 <= value <= 1, f"Value out of range: {value}. Must be between 0 and 1."
        # fmt: on
        self.__hue: float = hue
        self.__saturation: float = saturation
        self.__value: float = value

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_hue(self) -> float:
        """
        Retrieve the hue component of the HSV color.

        This method returns the hue component as a float in the range [0, 360].

        :return: The hue component of this HSVColor, as a float between 0 and 360.
        """
        return self.__hue

    def get_saturation(self) -> float:
        """
        Retrieve the saturation component of the HSV color.

        This method returns the saturation component as a float in the range [0, 1].

        :return: The saturation component of this HSVColor, as a float between 0 and 1.
        """
        return self.__saturation

    def get_value(self) -> float:
        """
        Retrieve the value component of the HSV color.

        This method returns the value component as a float in the range [0, 1].

        :return: The value component of this HSVColor, as a float between 0 and 1.
        """
        return self.__value

    def to_rgb_color(self) -> RGBColor:
        """
        Convert the current color representation to RGB format.

        This method transforms the current color into an equivalent RGB (Red, Green, Blue)
        representation. It returns a new RGBColor object containing the RGB components of
        the current color.

        :return: A new RGBColor object representing the current color in RGB format.
        """
        # Normalize hue to the range [0, 360)
        self.__hue %= 360

        if self.__saturation == 0:
            # Grayscale color (no saturation means R = G = B = Value)
            gray = round(self.__value * 255)
            return RGBColor(red=gray, green=gray, blue=gray)

        hi = math.floor(self.__hue / 60) % 6
        f = (self.__hue / 60) - hi
        p = self.__value * (1.0 - self.__saturation)
        q = self.__value * (1.0 - f * self.__saturation)
        t = self.__value * (1.0 - (1.0 - f) * self.__saturation)

        # Map HSV to RGB based on the region (hi)
        if hi == 0:
            r, g, b = self.__value, t, p
        elif hi == 1:
            r, g, b = q, self.__value, p
        elif hi == 2:
            r, g, b = p, self.__value, t
        elif hi == 3:
            r, g, b = p, q, self.__value
        elif hi == 4:
            r, g, b = t, p, self.__value
        elif hi == 5:
            r, g, b = self.__value, p, q
        else:
            raise ValueError("Unexpected value for hi during HSV to RGB conversion.")

        # Convert to integer RGB values using rounding
        return RGBColor(red=round(r * 255), green=round(g * 255), blue=round(b * 255))
