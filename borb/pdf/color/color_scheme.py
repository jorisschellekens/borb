#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A class that provides static methods to generate color schemes based on the HSV color model."""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.hsv_color import HSVColor


class ColorScheme:
    """A class that provides static methods to generate color schemes based on the HSV color model."""

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def analogous_colors(
        base_color: Color, angle_in_degrees: float = 30
    ) -> typing.List[Color]:
        """
        Generate analogous colors for a given color.

        :param base_color:          The base Color.
        :param angle_in_degrees:    The angle (in degrees) between the base color and each analogous color.
        :return:                    A list of two Color objects representing the analogous colors.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=(hsv_color.get_hue() - angle_in_degrees) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
            HSVColor(
                hue=(hsv_color.get_hue() + angle_in_degrees) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
        ]

    @staticmethod
    def complementary_color(base_color: Color) -> Color:
        """
        Generate the complementary color for a given color.

        :param base_color:  The base color.
        :return:            A new HSVColor object representing the complementary color.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        complementary_hue = (hsv_color.get_hue() + 180) % 360
        return HSVColor(
            hue=complementary_hue,
            saturation=hsv_color.get_saturation(),
            value=hsv_color.get_value(),
        )

    @staticmethod
    def monochromatic(base_color: Color, steps: int = 5) -> typing.List[HSVColor]:
        """
        Generate a monochromatic color scheme based on a single hue.

        :param base_color:  The base Color to generate the scheme from.
        :param steps:       The number of variations to generate.
        :return:            A list of Color objects in the monochromatic scheme.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=hsv_color.get_hue(),
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value() * (i / steps),
            )
            for i in range(1, steps + 1)
        ]

    @staticmethod
    def shades(base_color: Color, steps: int = 5) -> typing.List[Color]:
        """
        Generate shades of a given color (mixing with black).

        :param base_color:  The base HSVColor to generate shades from.
        :param steps:       The number of shades to generate.
        :return:            A list of HSVColor objects representing shades.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=hsv_color.get_hue(),
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value() * (i / steps),
            )
            for i in range(1, steps + 1)
        ]

    @staticmethod
    def split_complementary_colors(
        base_color: Color, angle: float = 30
    ) -> typing.List[Color]:
        """
        Generate split complementary colors for a given color.

        :param base_color:  The base Color.
        :param angle:       The angle (in degrees) between the base color and each split complementary color.
        :return:            A list of two HSVColor objects representing the split complementary colors.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=(hsv_color.get_hue() + 180 - angle) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
            HSVColor(
                hue=(hsv_color.get_hue() + 180 + angle) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
        ]

    @staticmethod
    def square_colors(base_color: Color) -> typing.List[Color]:
        """
        Generate square colors for a given color.

        :param base_color:  The base Color.
        :return:            A list of three Color objects representing the square colors.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=(hsv_color.get_hue() + 90) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
            HSVColor(
                hue=(hsv_color.get_hue() + 180) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
            HSVColor(
                hue=(hsv_color.get_hue() + 270) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
        ]

    @staticmethod
    def tetradic_colors(base_color: Color) -> typing.List[Color]:
        """
        Generate tetradic (rectangle) colors for a given color.

        :param base_color:  The base Color.
        :return:            A list of three Color objects representing the tetradic colors.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=(hsv_color.get_hue() + 90) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
            HSVColor(
                hue=(hsv_color.get_hue() + 180) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
            HSVColor(
                hue=(hsv_color.get_hue() + 270) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
        ]

    @staticmethod
    def tints(base_color: Color, steps: int = 5) -> typing.List[Color]:
        """
        Generate tints of a given color (mixing with white).

        :param base_color:  The base Color to generate tints from.
        :param steps:       The number of tints to generate.
        :return:            A list of Color objects representing tints.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=hsv_color.get_hue(),
                saturation=hsv_color.get_saturation() * (1.0 - (i / steps)),
                value=hsv_color.get_value(),
            )
            for i in range(1, steps + 1)
        ]

    @staticmethod
    def triadic_colors(base_color: Color) -> typing.List[Color]:
        """
        Generate triadic colors for a given color.

        :param base_color:  The base Color.
        :return:            A list of two Color objects representing the triadic colors.
        """
        hsv_color: HSVColor = base_color.to_rgb_color().to_hsv_color()
        return [
            HSVColor(
                hue=(hsv_color.get_hue() + 120) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
            HSVColor(
                hue=(hsv_color.get_hue() + 240) % 360,
                saturation=hsv_color.get_saturation(),
                value=hsv_color.get_value(),
            ),
        ]
