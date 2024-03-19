#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module provides implementations of various colors and their respective colormodels,
    including: RGB, CMYK, grayscale, hex and X11
"""
import logging
import typing
from decimal import Decimal

from borb.io.read.types import Function
from borb.io.read.types import List
from borb.io.read.types import Name

logger = logging.getLogger(__name__)


class Color(object):
    """
    Color (American English), or colour (Commonwealth English),
    is the characteristic of visual perception described through color categories,
    with names such as red, orange, yellow, green, blue, or purple.
    This perception of color derives from the stimulation of photoreceptor cells
    (in particular cone cells in the human eye and other vertebrate eyes) by electromagnetic radiation
    (in the visible spectrum in the case of humans).
    Color categories and physical specifications of color are associated with objects through
    the wavelengths of the light that is reflected from them and their intensities.
    This reflection is governed by the object's physical properties such as light absorption, emission spectra, etc.
    """

    def to_rgb(self) -> "RGBColor":
        """
        This method returns the RGB representation of this Color
        :return:    the RGBColor equivalent of this Color
        """
        pass


class CMYKColor(Color):
    """
    The CMYK color model (also known as process color, or four color) is a subtractive color model, based on the CMY color model,
    used in color printing, and is also used to describe the printing process itself.
    CMYK refers to the four ink plates used in some color printing: cyan, magenta, yellow, and key (black).

    The CMYK model works by partially or entirely masking colors on a lighter, usually white, background.
    The ink reduces the light that would otherwise be reflected.
    Such a model is called subtractive because inks "subtract" the colors red, green and blue from white light.
    White light minus red leaves cyan, white light minus green leaves magenta, and white light minus blue leaves yellow.

    In additive color models, such as RGB, white is the "additive" combination of all primary colored lights, black is the absence of light.
    In the CMYK model, it is the opposite: white is the natural color of the paper or other background,
    black results from a full combination of colored inks.
    To save cost on ink, and to produce deeper black tones, unsaturated and dark colors are produced by using black ink
    instead of the combination of cyan, magenta, and yellow.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, c: Decimal, m: Decimal, y: Decimal, k: Decimal):
        self.cyan = c
        self.magenta = m
        self.yellow = y
        self.key = k

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        return CMYKColor(self.cyan, self.magenta, self.yellow, self.key)

    #
    # PUBLIC
    #

    @staticmethod
    def from_rgb(c: "RGBColor") -> "CMYKColor":
        """
        This method returns the CMYKColor representation of an RGB color
        :param c:   the origin RGBColor
        :return:    the matching CMYKColor
        """
        K: Decimal = Decimal(1.0) - max(c.red, c.green, c.blue)
        C: Decimal = (Decimal(1) - c.red - K) / (Decimal(1.0) - K)
        M: Decimal = (Decimal(1) - c.green - K) / (Decimal(1.0) - K)
        Y: Decimal = (Decimal(1) - c.blue - K) / (Decimal(1.0) - K)
        return CMYKColor(C, M, Y, K)

    def to_rgb(self) -> "RGBColor":
        """
        This method returns the RGB representation of this Color
        :return:    the RGBColor equivalent of this Color
        """
        ONE: Decimal = Decimal(1)
        r: Decimal = (ONE - self.cyan) * (ONE - self.key)
        g: Decimal = (ONE - self.magenta) * (ONE - self.key)
        b: Decimal = (ONE - self.yellow) * (ONE - self.key)
        return RGBColor(r, g, b)


class GrayColor(Color):
    """
    In digital photography, computer-generated imagery, and colorimetry,
    a grayscale or image is one in which the value of each pixel is a single sample representing only an amount of light;
    that is, it carries only intensity information.
    Grayscale images, a kind of black-and-white or gray monochrome, are composed exclusively of shades of gray.
    The contrast ranges from black at the weakest intensity to white at the strongest.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, g: Decimal):
        self.gray_level = g

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        return GrayColor(self.gray_level)

    #
    # PUBLIC
    #

    def to_rgb(self) -> "RGBColor":
        """
        This method returns the RGB representation of this Color
        :return:    the RGBColor equivalent of this Color
        """
        return RGBColor(self.gray_level, self.gray_level, self.gray_level)


class HSVColor(Color):
    """
    HSL (hue, saturation, lightness) and HSV (hue, saturation, value, also known as HSB or hue, saturation, brightness)
    are alternative representations of the RGB color model, designed in the 1970s by computer graphics researchers
    to more closely align with the way human vision perceives color-making attributes.
    In these models, colors of each hue are arranged in a radial slice,
    around a central axis of neutral colors which ranges from black at the bottom to white at the top.

    The HSL representation models the way different paints mix together to create colour in the real world,
    with the lightness dimension resembling the varying amounts of black or white paint in the mixture
    (e.g. to create "light red", a red pigment can be mixed with white paint;
    this white paint corresponds to a high "lightness" value in the HSL representation).
    Fully saturated colors are placed around a circle at a lightness value of ½,
    with a lightness value of 0 or 1 corresponding to fully black or white, respectively.

    Meanwhile, the HSV representation models how colors appear under light.
    The difference between HSL and HSV is that a color with maximum lightness in HSL is pure white,
    but a color with maximum value/brightness in HSV is analogous to shining a white light on a colored object
    (e.g. shining a bright white light on a red object causes the object to still appear red, just brighter and more intense,
    while shining a dim light on a red object causes the object to appear darker and less bright).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, hue: Decimal, saturation: Decimal, value: Decimal):
        self.hue = hue
        self.saturation = saturation
        self.value = value

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        return HSVColor(self.hue, self.saturation, self.value)

    #
    # PUBLIC
    #

    @staticmethod
    def analogous(color: Color) -> typing.List[Color]:
        """
        This function returns an analogous color scheme.
        Analogous color schemes use colors that are next to each other on the color wheel. They usually match well and create serene and comfortable designs.
        Analogous color schemes are often found in nature and are harmonious and pleasing to the eye.
        :param color:   the input Color
        :return:        an analogous Color
        """
        c: HSVColor = HSVColor.from_rgb(color.to_rgb())
        return [
            HSVColor(Decimal((int(c.hue * 360 + a) % 360) / 360), c.saturation, c.value)
            for a in [0, 15, 30]
        ]

    @staticmethod
    def complementary(color: Color) -> Color:
        """
        This function returns an HSV color whose hue is the complement of the current HSV color
        :param color:   the input Color
        :return:        a complementary Color
        """
        c: HSVColor = HSVColor.from_rgb(color.to_rgb())
        new_hue: int = int(float(c.hue) * 360.0) + 180 % 360
        return HSVColor(Decimal(new_hue / 360), c.saturation, c.value)

    def darker(self) -> "HSVColor":
        """
        This function returns a darker shade of the current HSV color
        :return:    a darker shade of this Color
        """
        return HSVColor(self.hue, self.saturation, self.value * Decimal(0.8))

    @staticmethod
    def from_rgb(c: "RGBColor") -> "HSVColor":
        """
        This method returns the HSV representation of an RGB color
        """
        r, g, b = c.red, c.green, c.blue
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = Decimal(0)
        elif mx == r:
            h = (Decimal(60) * ((g - b) / df) + Decimal(360)) % Decimal(360)
        elif mx == g:
            h = (Decimal(60) * ((b - r) / df) + Decimal(120)) % Decimal(360)
        elif mx == b:
            h = (Decimal(60) * ((r - g) / df) + Decimal(240)) % Decimal(360)
        if mx == 0:
            s = Decimal(0)
        else:
            s = (df / mx) * 100
        v = mx * 100
        HUNDRED = Decimal(100)
        FULL_CIRCLE = Decimal(360)
        return HSVColor(h / FULL_CIRCLE, s / HUNDRED, v / HUNDRED)

    @staticmethod
    def split_complementary(color: Color) -> typing.List[Color]:
        """
        This function returns a split complementary color scheme.
        A split complementary color scheme uses two colors plus the color that is opposite to them on the color wheel.
        For example blue and purple with yellow.
        :param color:       the complementary color
        :return:            3 colors (a split complementary color scheme)
        """
        c: HSVColor = HSVColor.from_rgb(color.to_rgb())
        return [
            HSVColor(Decimal((int(c.hue * 360 + a) % 360) / 360), c.saturation, c.value)
            for a in [0, 165, 195]
        ]

    @staticmethod
    def tetradic_rectangle(c: Color) -> typing.List[Color]:
        """
        This function returns a tetradic (rectangular) color scheme.
        The rectangle or tetradic color scheme uses four colors arranged into two complementary pairs.
        This rich color scheme offers plenty of possibilities for variation.
        Tetradic color schemes works best if you let one color be dominant.
        :param c:   one color of one of the complementary paris
        :return:    four colors (two complementary pairs)
        """
        c0: HSVColor = HSVColor.from_rgb(c.to_rgb())
        return [
            HSVColor(
                Decimal((int(c0.hue * 360 + a) % 360) / 360), c0.saturation, c0.value
            )
            for a in [0, 30, 180, 210]
        ]

    @staticmethod
    def tetradic_square(color: Color) -> typing.List[Color]:
        """
        This function returns a tetradic (square) color scheme.
        This harmony is comparable to the Tetradic harmony but with the four colors spaced evenly around the color wheel.
        This harmony works best if one color dominates.
        Just like the Tetradic harmony, you need to keep track of the relationship between the cool and the warm colors.
        :param color:
        :return:        four colors (a tetradic square color scheme)
        """
        c: HSVColor = HSVColor.from_rgb(color.to_rgb())
        return [
            HSVColor(Decimal((int(c.hue * 360 + a) % 360) / 360), c.saturation, c.value)
            for a in [0, 90, 180, 270]
        ]

    def to_rgb(self) -> "RGBColor":
        """
        This method returns the RGB representation of this Color
        :return:    the RGBColor equivalent of this Color
        """
        h, s, v = self.hue, self.saturation, self.value
        ONE = Decimal(1)
        SIX = Decimal(6)
        if s == 0:
            return RGBColor(Decimal(v), Decimal(v), Decimal(v))
        i = int(h * SIX)  # XXX assume int() truncates!
        f = (h * SIX) - i
        p, q, t = v * (ONE - s), v * (ONE - s * f), v * (ONE - s * (ONE - f))
        i %= 6
        if i == 0:
            return RGBColor(Decimal(v), Decimal(t), Decimal(p))
        if i == 1:
            return RGBColor(Decimal(q), Decimal(v), Decimal(p))
        if i == 2:
            return RGBColor(Decimal(p), Decimal(v), Decimal(t))
        if i == 3:
            return RGBColor(Decimal(p), Decimal(q), Decimal(v))
        if i == 4:
            return RGBColor(Decimal(t), Decimal(p), Decimal(v))
        if i == 5:
            return RGBColor(Decimal(v), Decimal(p), Decimal(q))
        return RGBColor(Decimal(0), Decimal(0), Decimal(0))

    @staticmethod
    def triadic(color: Color) -> typing.List[Color]:
        """
        This function returns a triadic color scheme.
        A triadic color scheme uses colors that are evenly spaced around the color wheel.
        Triadic color harmonies tend to be quite vibrant, even if you use pale or unsaturated versions of your hues.
        To use a triadic harmony successfully, the colors should be carefully balanced - let one color dominate and use the two others for accent.
        """
        c: HSVColor = HSVColor.from_rgb(color.to_rgb())
        return [
            HSVColor(Decimal((int(c.hue * 360 + a) % 360) / 360), c.saturation, c.value)
            for a in [0, 60, 120]
        ]


class RGBColor(Color):
    """
    An RGB color space is any additive color space based on the RGB color model.
    A particular color space that employs RGB primaries for part of its specification is defined by the three chromaticities of the red, green, and blue additive primaries,
    and can produce any chromaticity that is the 2D triangle defined by those primary colors (ie. excluding transfer function, white point, etc.).
    The primary colors are specified in terms of their CIE 1931 color space chromaticity coordinates (x,y), linking them to human-visible color.
    RGB is an abbreviation for red–green–blue.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, r: Decimal, g: Decimal, b: Decimal):
        assert 0 <= r <= 1
        assert 0 <= g <= 1
        assert 0 <= b <= 1
        self.red: Decimal = r
        self.green: Decimal = g
        self.blue: Decimal = b

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        return RGBColor(self.red, self.green, self.blue)

    #
    # PUBLIC
    #

    def to_hex_string(self):
        """
        This method returns a hexadecimal string representing the RGB color
        """
        return "#{:02x}{:02x}{:02x}".format(
            int(self.red * 255), int(self.green * 255), int(self.blue * 255)
        )

    def to_rgb(self):
        """
        This method returns the RGB representation of this Color
        """
        return self


class HexColor(RGBColor):
    """
    A hex triplet is a six-digit, three-byte hexadecimal number used in HTML, CSS, SVG, and other computing applications to represent colors.
    The bytes represent the red, green, and blue components of the color.
    One byte represents a number in the range 00 to FF (in hexadecimal notation), or 0 to 255 in decimal notation.
    This represents the least (0) to the most (255) intensity of each of the color components.

    Thus web colors specify colors in the 24-bit RGB color scheme.

    The hex triplet is formed by concatenating three bytes in hexadecimal notation, in the following order:
    - Byte 1: red value (color type red)
    - Byte 2: green value (color type green)
    - Byte 3: blue value (color type blue)
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, hex_string: str):
        if hex_string.startswith("#"):
            hex_string = hex_string[1:]
        if len(hex_string) == 3:
            hex_string = f"{hex_string[0]}{hex_string[0]}{hex_string[1]}{hex_string[1]}{hex_string[2]}{hex_string[2]}"
        assert len(hex_string) == 6 or len(hex_string) == 8
        r: float = 0
        g: float = 0
        b: float = 0
        a: float = 0
        if len(hex_string) == 6:
            a = 255
            r = int(hex_string[0:2], 16)
            g = int(hex_string[2:4], 16)
            b = int(hex_string[4:6], 16)
        if len(hex_string) == 8:
            a = int(hex_string[0:2], 16)
            r = int(hex_string[2:4], 16)
            g = int(hex_string[4:6], 16)
            b = int(hex_string[6:8], 16)
        a /= 255
        r /= 255
        g /= 255
        b /= 255
        super(HexColor, self).__init__(Decimal(r), Decimal(g), Decimal(b))

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        return HexColor(self.to_hex_string())

    def __eq__(self, other):
        return (
            isinstance(other, HexColor)
            and other.to_hex_string() == self.to_hex_string()
        )

    def __hash__(self):
        return hash(self.to_hex_string())

    #
    # PUBLIC
    #


class Separation(Color):
    """
    When printing a page, most devices produce a single composite page on which all process colorants (and spot
    colorants, if any) are combined. However, some devices, such as imagesetters, produce a separate,
    monochromatic rendition of the page, called a separation, for each colorant. When the separations are later
    combined—on a printing press, for example—and the proper inks or other colorants are applied to them, the
    result is a full-colour page.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, color_space: typing.List[typing.Any], xs: typing.List[Decimal]):
        super(Separation, self).__init__()
        self.color_space = color_space
        self.xs = xs
        self._to_rgb_cache: typing.Optional[RGBColor] = None
        """"
        except Exception as ex:
            if len(color_space) != 0 and len(xs) != 0:
                logger.debug("Unable to instantiate separation color, defaulting to black")
            self.rgb_color = RGBColor(Decimal(0), Decimal(0), Decimal(0))
            pass
        """

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        out: Separation = Separation([], [])
        out._to_rgb_cache = self.to_rgb()
        return out

    #
    # PUBLIC
    #

    def to_rgb(self) -> "RGBColor":
        """
        This method returns the RGB representation of this Color
        """
        if self._to_rgb_cache is not None:
            return self._to_rgb_cache

        assert isinstance(self.color_space[3], Function)
        tint_function: Function = self.color_space[3]

        # run function
        try:
            ys: typing.List[Decimal] = tint_function.evaluate(self.xs)
            assert ys is not None
        except:
            logger.info(
                "Unable to execute TintFunction for Separation %d, defaulting to black"
                % id(self)
            )
            self._to_rgb_cache = RGBColor(Decimal(0), Decimal(0), Decimal(0))
            return self._to_rgb_cache

        # determine the color space to map to
        alternative_color_space: typing.Optional[Name] = None
        if isinstance(self.color_space[2], Name):
            alternative_color_space = self.color_space[2]
        if (
            isinstance(self.color_space[2], List)
            and len(self.color_space[2]) == 2
            and isinstance(self.color_space[2][0], Name)
        ):
            alternative_color_space = self.color_space[2][0]

        # DeviceCMYK
        if alternative_color_space == "DeviceCMYK":
            self._to_rgb_cache = CMYKColor(ys[0], ys[1], ys[2], ys[3]).to_rgb()
            return self._to_rgb_cache

        # DeviceRGB
        if alternative_color_space == "DeviceRGB":
            self._to_rgb_cache = RGBColor(ys[0], ys[1], ys[2])
            return self._to_rgb_cache

        # ICCBased
        if alternative_color_space == "ICCBased":
            if len(ys) == 1:
                self._to_rgb_cache = GrayColor(ys[0]).to_rgb()
            if len(ys) == 3:
                self._to_rgb_cache = RGBColor(ys[0], ys[1], ys[2])
            if len(ys) == 4:
                self._to_rgb_cache = CMYKColor(ys[0], ys[1], ys[2], ys[3]).to_rgb()
            assert self._to_rgb_cache is not None
            return self._to_rgb_cache

        # default
        return RGBColor(Decimal(0), Decimal(0), Decimal(0))


class X11Color(HexColor):
    """
    In computing, on the X Window System, X11 color names are represented in a simple text file,
    which maps certain strings to RGB color values.
    It was traditionally shipped with every X11 installation,
    hence the name, and is usually located in <X11root>/lib/X11/rgb.txt.
    The web colors list is descended from it but differs for certain color names.
    """

    COLOR_DEFINITION = {
        "AliceBlue": "#FFF0F8FF",
        "AntiqueWhite": "#FFFAEBD7",
        "Aqua": "#FF00FFFF",
        "Aquamarine": "#FF7FFFD4",
        "Azure": "#FFF0FFFF",
        "Beige": "#FFF5F5DC",
        "Bisque": "#FFFFE4C4",
        "Black": "#FF000000",
        "BlanchedAlmond": "#FFFFEBCD",
        "Blue": "#FF0000FF",
        "BlueViolet": "#FF8A2BE2",
        "Brown": "#FFA52A2A",
        "BurlyWood": "#FFDEB887",
        "CadetBlue": "#FF5F9EA0",
        "Chartreuse": "#FF7FFF00",
        "Chocolate": "#FFD2691E",
        "Coral": "#FFFF7F50",
        "CornflowerBlue": "#FF6495ED",
        "Cornsilk": "#FFFFF8DC",
        "Crimson": "#FFDC143C",
        "Cyan": "#FF00FFFF",
        "DarkBlue": "#FF00008B",
        "DarkCyan": "#FF008B8B",
        "DarkGoldenrod": "#FFB8860B",
        "DarkGray": "#FFA9A9A9",
        "DarkGreen": "#FF006400",
        "DarkKhaki": "#FFBDB76B",
        "DarkMagenta": "#FF8B008B",
        "DarkOliveGreen": "#FF556B2F",
        "DarkOrange": "#FFFF8C00",
        "DarkOrchid": "#FF9932CC",
        "DarkRed": "#FF8B0000",
        "DarkSalmon": "#FFE9967A",
        "DarkSeaGreen": "#FF8FBC8F",
        "DarkSlateBlue": "#FF483D8B",
        "DarkSlateGray": "#FF2F4F4F",
        "DarkTurquoise": "#FF00CED1",
        "DarkViolet": "#FF9400D3",
        "DeepPink": "#FFFF1493",
        "DeepSkyBlue": "#FF00BFFF",
        "DimGray": "#FF696969",
        "DodgerBlue": "#FF1E90FF",
        "Firebrick": "#FFB22222",
        "FloralWhite": "#FFFFFAF0",
        "ForestGreen": "#FF228B22",
        "Fuchsia": "#FFFF00FF",
        "Gainsboro": "#FFDCDCDC",
        "GhostWhite": "#FFF8F8FF",
        "Gold": "#FFFFD700",
        "Goldenrod": "#FFDAA520",
        "Gray": "#FF808080",
        "Green": "#FF008000",
        "GreenYellow": "#FFADFF2F",
        "Honeydew": "#FFF0FFF0",
        "HotPink": "#FFFF69B4",
        "IndianRed": "#FFCD5C5C",
        "Indigo": "#FF4B0082",
        "Ivory": "#FFFFFFF0",
        "Khaki": "#FFF0E68C",
        "Lavender": "#FFE6E6FA",
        "LavenderBlush": "#FFFFF0F5",
        "LawnGreen": "#FF7CFC00",
        "LemonChiffon": "#FFFFFACD",
        "LightBlue": "#FFADD8E6",
        "LightCoral": "#FFF08080",
        "LightCyan": "#FFE0FFFF",
        "LightGoldenrodYellow": "#FFFAFAD2",
        "LightGray": "#FFD3D3D3",
        "LightGreen": "#FF90EE90",
        "LightPink": "#FFFFB6C1",
        "LightSalmon": "#FFFFA07A",
        "LightSeaGreen": "#FF20B2AA",
        "LightSkyBlue": "#FF87CEFA",
        "LightSlateGray": "#FF778899",
        "LightSteelBlue": "#FFB0C4DE",
        "LightYellow": "#FFFFFFE0",
        "Lime": "#FF00FF00",
        "LimeGreen": "#FF32CD32",
        "Linen": "#FFFAF0E6",
        "Magenta": "#FFFF00FF",
        "Maroon": "#FF800000",
        "MediumAquamarine": "#FF66CDAA",
        "MediumBlue": "#FF0000CD",
        "MediumOrchid": "#FFBA55D3",
        "MediumPurple": "#FF9370DB",
        "MediumSeaGreen": "#FF3CB371",
        "MediumSlateBlue": "#FF7B68EE",
        "MediumSpringGreen": "#FF00FA9A",
        "MediumTurquoise": "#FF48D1CC",
        "MediumVioletRed": "#FFC71585",
        "MidnightBlue": "#FF191970",
        "MintCream": "#FFF5FFFA",
        "MistyRose": "#FFFFE4E1",
        "Moccasin": "#FFFFE4B5",
        "NavajoWhite": "#FFFFDEAD",
        "Navy": "#FF000080",
        "OldLace": "#FFFDF5E6",
        "Olive": "#FF808000",
        "OliveDrab": "#FF6B8E23",
        "Orange": "#FFFFA500",
        "OrangeRed": "#FFFF4500",
        "Orchid": "#FFDA70D6",
        "PaleGoldenrod": "#FFEEE8AA",
        "PaleGreen": "#FF98FB98",
        "PaleTurquoise": "#FFAFEEEE",
        "PaleVioletRed": "#FFDB7093",
        "PapayaWhip": "#FFFFEFD5",
        "PeachPuff": "#FFFFDAB9",
        "Peru": "#FFCD853F",
        "Pink": "#FFFFC0CB",
        "Plum": "#FFDDA0DD",
        "PowderBlue": "#FFB0E0E6",
        "Purple": "#FF800080",
        "Red": "#FFFF0000",
        "RosyBrown": "#FFBC8F8F",
        "RoyalBlue": "#FF4169E1",
        "SaddleBrown": "#FF8B4513",
        "Salmon": "#FFFA8072",
        "SandyBrown": "#FFF4A460",
        "SeaGreen": "#FF2E8B57",
        "SeaShell": "#FFFFF5EE",
        "Sienna": "#FFA0522D",
        "Silver": "#FFC0C0C0",
        "SkyBlue": "#FF87CEEB",
        "SlateBlue": "#FF6A5ACD",
        "SlateGray": "#FF708090",
        "Snow": "#FFFFFAFA",
        "SpringGreen": "#FF00FF7F",
        "SteelBlue": "#FF4682B4",
        "Tan": "#FFD2B48C",
        "Teal": "#FF008080",
        "Thistle": "#FFD8BFD8",
        "Tomato": "#FFFF6347",
        "Transparent": "#00FFFFFF",
        "Turquoise": "#FF40E0D0",
        "Violet": "#FFEE82EE",
        "Wheat": "#FFF5DEB3",
        "White": "#FFFFFFFF",
        "WhiteSmoke": "#FFF5F5F5",
        "Yellow": "#FFFFFF00",
        "YellowGreen": "#FF9ACD32",
    }

    #
    # CONSTRUCTOR
    #

    def __init__(self, color_name: str):
        assert color_name in X11Color.COLOR_DEFINITION
        self.color_name: str = color_name
        super(X11Color, self).__init__(X11Color.COLOR_DEFINITION[color_name])

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        return X11Color(self.color_name)

    #
    # PUBLIC
    #

    @staticmethod
    def find_nearest_x11_color(color: Color) -> "X11Color":
        """
        This function find the nearest X11Color equivalent for a given Color
        """
        rgb_color_001: RGBColor = color.to_rgb()
        d_min: typing.Optional[Decimal] = None
        c_min: typing.Optional[str] = None
        for n, c in X11Color.COLOR_DEFINITION.items():
            rgb_color_002: RGBColor = HexColor(c)
            d: Decimal = (
                (rgb_color_001.red - rgb_color_002.red) ** 2
                + (rgb_color_001.green - rgb_color_002.green) ** 2
                + (rgb_color_001.blue - rgb_color_002.blue) ** 2
            )
            if d_min is None or d < d_min:
                d_min = d
                c_min = n
        assert d_min is not None
        assert c_min is not None
        return X11Color(c_min)

    def get_name(self) -> str:
        """
        This function returns the name of this X11Color
        """
        return self.color_name
