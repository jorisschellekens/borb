#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a color defined by X11 color names.

In computing, the X Window System (X11) uses a simple text file to map
specific color names to their corresponding RGB values. This file, commonly
located in `<X11root>/lib/X11/rgb.txt`, has traditionally been included
with every X11 installation.

The list of web colors is derived from the X11 color names but may differ
in certain entries, reflecting variations in naming conventions across
different platforms.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.hex_color import HexColor


class X11Color:
    """
    Represents a color defined by X11 color names.

    In computing, the X Window System (X11) uses a simple text file to map
    specific color names to their corresponding RGB values. This file, commonly
    located in `<X11root>/lib/X11/rgb.txt`, has traditionally been included
    with every X11 installation.

    The list of web colors is derived from the X11 color names but may differ
    in certain entries, reflecting variations in naming conventions across
    different platforms.
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

    ALICE_BLUE = HexColor("#F0F8FF")
    ANTIQUE_WHITE = HexColor("#FAEBD7")
    AQUA = HexColor("#00FFFF")
    AQUAMARINE = HexColor("#7FFFD4")
    AZURE = HexColor("#F0FFFF")

    BEIGE = HexColor("#F5F5DC")
    BISQUE = HexColor("#FFE4C4")
    BLACK = HexColor("#000000")
    BLANCHED_ALMOND = HexColor("#FFEBCD")
    BLUE = HexColor("#0000FF")
    BLUE_VIOLET = HexColor("#8A2BE2")
    BROWN = HexColor("#A52A2A")
    BURLY_WOOD = HexColor("#DEB887")

    CADET_BLUE = HexColor("#5F9EA0")
    CHARTREUSE = HexColor("#7FFF00")
    CHOCOLATE = HexColor("#D2691E")
    CORAL = HexColor("#FF7F50")
    CORNFLOWER_BLUE = HexColor("#6495ED")
    CORNSILK = HexColor("#FFF8DC")
    CRIMSON = HexColor("#DC143C")
    CYAN = HexColor("#00FFFF")

    DARK_BLUE = HexColor("#00008B")
    DARK_CYAN = HexColor("#008B8B")
    DARK_GOLDENROD = HexColor("#B8860B")
    DARK_GRAY = HexColor("#A9A9A9")
    DARK_GREEN = HexColor("#006400")
    DARK_KHAKI = HexColor("#BDB76B")
    DARK_MAGENTA = HexColor("#8B008B")
    DARK_OLIVE_GREEN = HexColor("#556B2F")
    DARK_ORANGE = HexColor("#FF8C00")
    DARK_ORCHID = HexColor("#9932CC")
    DARK_RED = HexColor("#8B0000")
    DARK_SALMON = HexColor("#E9967A")
    DARK_SEA_GREEN = HexColor("#8FBC8F")
    DARK_SLATE_BLUE = HexColor("#483D8B")
    DARK_SLATE_GRAY = HexColor("#2F4F4F")
    DARK_TURQUOISE = HexColor("#00CED1")
    DARK_VIOLET = HexColor("#9400D3")
    DEEP_PINK = HexColor("#FF1493")
    DEEP_SKY_BLUE = HexColor("#00BFFF")
    DIM_GRAY = HexColor("#696969")
    DODGER_BLUE = HexColor("#1E90FF")

    FIREBRICK = HexColor("#B22222")
    FIRE_OPAL = HexColor("#DE6449")
    FLORAL_WHITE = HexColor("#FFFAF0")
    FOREST_GREEN = HexColor("#228B22")
    FUCHSIA = HexColor("#FF00FF")

    GAINSBORO = HexColor("#DCDCDC")
    GHOST_WHITE = HexColor("#F8F8FF")
    GOLD = HexColor("#FFD700")
    GOLDENROD = HexColor("#DAA520")
    GRAY = HexColor("#808080")
    GREEN = HexColor("#008000")
    GREEN_YELLOW = HexColor("#ADFF2F")

    HONEYDEW = HexColor("#F0FFF0")
    HOT_PINK = HexColor("#FF69B4")

    INDIAN_RED = HexColor("#CD5C5C")
    INDIGO = HexColor("#4B0082")
    IVORY = HexColor("#FFFFF0")

    KHAKI = HexColor("#F0E68C")

    LAVENDER = HexColor("#E6E6FA")
    LAVENDER_BLUSH = HexColor("#FFF0F5")
    LAWN_GREEN = HexColor("#7CFC00")
    LEMON_CHIFFON = HexColor("#FFFACD")
    LIGHT_BLUE = HexColor("#ADD8E6")
    LIGHT_CORAL = HexColor("#F08080")
    LIGHT_CYAN = HexColor("#E0FFFF")
    LIGHT_GOLDENROD_YELLOW = HexColor("#FAFAD2")
    LIGHT_GRAY = HexColor("#D3D3D3")
    LIGHT_GREEN = HexColor("#90EE90")
    LIGHT_PINK = HexColor("#FFB6C1")
    LIGHT_SALMON = HexColor("#FFA07A")
    LIGHT_SEA_GREEN = HexColor("#20B2AA")
    LIGHT_SKY_BLUE = HexColor("#87CEFA")
    LIGHT_SLATE_GRAY = HexColor("#778899")
    LIGHT_STEEL_BLUE = HexColor("#B0C4DE")
    LIGHT_YELLOW = HexColor("#FFFFE0")
    LIME = HexColor("#00FF00")
    LIME_GREEN = HexColor("#32CD32")
    LINEN = HexColor("#FAF0E6")

    MAGENTA = HexColor("#FF00FF")
    MAROON = HexColor("#800000")
    MEDIUM_AQUAMARINE = HexColor("#66CDAA")
    MEDIUM_BLUE = HexColor("#0000CD")
    MEDIUM_ORCHID = HexColor("#BA55D3")
    MEDIUM_PURPLE = HexColor("#9370DB")
    MEDIUM_SEA_GREEN = HexColor("#3CB371")
    MEDIUM_SLATE_BLUE = HexColor("#7B68EE")
    MEDIUM_SPRING_GREEN = HexColor("#00FA9A")
    MEDIUM_TURQUOISE = HexColor("#48D1CC")
    MEDIUM_VIOLET_RED = HexColor("#C71585")
    MIDNIGHT_BLUE = HexColor("#191970")
    MINT_CREAM = HexColor("#F5FFFA")
    MISTY_ROSE = HexColor("#FFE4E1")
    MOCCASIN = HexColor("#FFE4B5")

    NAVAJO_WHITE = HexColor("#FFDEAD")
    NAVY = HexColor("#000080")

    OLD_LACE = HexColor("#FDF5E6")
    OLIVE = HexColor("#808000")
    OLIVE_DRAB = HexColor("#6B8E23")
    ORANGE = HexColor("#FFA500")
    ORANGE_RED = HexColor("#FF4500")
    ORCHID = HexColor("#DA70D6")

    PALE_GOLDENROD = HexColor("#EEE8AA")
    PALE_GREEN = HexColor("#98FB98")
    PALE_TURQUOISE = HexColor("#AFEEEE")
    PALE_VIOLET_RED = HexColor("#DB7093")
    PAPAYA_WHIP = HexColor("#FFEFD5")
    PEACH_PUFF = HexColor("#FFDAB9")
    PERU = HexColor("#CD853F")
    PINK = HexColor("#FFC0CB")
    PLUM = HexColor("#DDA0DD")
    POWDER_BLUE = HexColor("#B0E0E6")
    PRUSSIAN_BLUE = HexColor("#0b3954")
    PURPLE = HexColor("#800080")

    RED = HexColor("#FF0000")
    ROSY_BROWN = HexColor("#BC8F8F")
    ROYAL_BLUE = HexColor("#4169E1")

    SADDLE_BROWN = HexColor("#8B4513")
    SALMON = HexColor("#FA8072")
    SANDY_BROWN = HexColor("#F4A460")
    SEA_GREEN = HexColor("#2E8B57")
    SEASHELL = HexColor("#FFF5EE")
    SIENNA = HexColor("#A0522D")
    SILVER = HexColor("#C0C0C0")
    SKY_BLUE = HexColor("#87CEEB")
    SLATE_BLUE = HexColor("#6A5ACD")
    SLATE_GRAY = HexColor("#708090")
    SNOW = HexColor("#FFFAFA")
    SPRING_GREEN = HexColor("#00FF7F")
    STEEL_BLUE = HexColor("#4682B4")

    TAN = HexColor("#D2B48C")
    TEAL = HexColor("#008080")
    THISTLE = HexColor("#D8BFD8")
    TOMATO = HexColor("#FF6347")
    TURQUOISE = HexColor("#40E0D0")

    VIOLET = HexColor("#EE82EE")

    WHEAT = HexColor("#F5DEB3")
    WHITE = HexColor("#FFFFFF")
    WHITE_SMOKE = HexColor("#F5F5F5")

    YELLOW = HexColor("#FFFF00")
    YELLOW_GREEN = HexColor("#9ACD32")
    YELLOW_MUNSELL = HexColor("#F1CD2E")

    @staticmethod
    def get_matching_color(color: Color) -> typing.Tuple[str, Color]:
        """
        Find the closest X11 color that visually matches the given color.

        This method accepts a `Color` object and determines the closest
        `X11Color` based on visual similarity. It returns a tuple
        containing the name of the closest matching X11 color and
        the corresponding `X11Color` object.

        :param color: The `Color` object to match.
        :return: A tuple consisting of the name of the closest
                 X11 color and the corresponding `X11Color` object.
        """
        from borb.pdf.color.rgb_color import RGBColor

        rgb_color_0: RGBColor = color.to_rgb_color()
        min_distance: typing.Optional[int] = None
        min_color_name: typing.Optional[str] = None
        min_color: typing.Optional[Color] = None
        for name in dir(X11Color):
            try:
                rgb_color_1: RGBColor = getattr(X11Color, name)
                distance = (
                    (rgb_color_0.get_red() - rgb_color_1.get_red()) ** 2
                    + (rgb_color_0.get_green() - rgb_color_1.get_green()) ** 2
                    + (rgb_color_0.get_blue() - rgb_color_1.get_blue()) ** 2
                )
                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    min_color_name = name
                    min_color = rgb_color_1
            except:
                pass
        # fmt: off
        assert min_color_name is not None, "No matching color name was found; min_color_name is None."
        assert min_color is not None, "No matching color object was found; min_color is None."
        # fmt: on
        return min_color_name, min_color
