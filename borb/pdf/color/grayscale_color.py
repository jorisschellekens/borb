#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a color in the grayscale color model, where each pixel carries only light intensity information.

In digital photography, computer-generated imagery, and colorimetry, a grayscale image is one in which each pixel
is a single sample representing an amount of light, carrying only intensity information. Grayscale images, also
known as black-and-white or gray monochrome images, are composed exclusively of shades of gray. The contrast
ranges from black (weakest intensity) to white (strongest intensity).
"""
from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor


class GrayscaleColor(Color):
    """
    Represents a color in the grayscale color model, where each pixel carries only light intensity information.

    In digital photography, computer-generated imagery, and colorimetry, a grayscale image is one in which each pixel
    is a single sample representing an amount of light, carrying only intensity information. Grayscale images, also
    known as black-and-white or gray monochrome images, are composed exclusively of shades of gray. The contrast
    ranges from black (weakest intensity) to white (strongest intensity).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, level: float):
        """
        Initialize a GrayscaleColor object with a specified intensity level.

        The `GrayscaleColor` class represents a color in grayscale,
        where the intensity level is a float between 0 and 1.
        A level of 0 corresponds to black, and a level of 1 corresponds to white.

        :param level: The intensity level of the grayscale color, must be between 0 (black) and 1 (white).
        """
        super().__init__()
        # fmt: off
        assert 0 <= level <= 1, f"Grayscale intensity level out of range: {level}. Must be between 0 and 1."
        # fmt: on
        self.__level: float = level

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_level(self) -> float:
        """
        Return the level component of this GrayscaleColor, as a float between 0 and 1.

        :return: The level component of this GrayscaleColor.
        """
        return self.__level

    def to_rgb_color(self) -> RGBColor:
        """
        Convert the current color representation to RGB format.

        This method transforms the current color into an equivalent RGB (Red, Green, Blue)
        representation. It returns a new RGBColor object containing the RGB components of
        the current color.

        :return: A new RGBColor object representing the current color in RGB format.
        """
        return RGBColor(
            red=int(self.__level * 255),
            green=int(self.__level * 255),
            blue=int(self.__level * 255),
        )
