from decimal import Decimal


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
        """
        pass


class RGBColor(Color):
    """
    An RGB color space is any additive color space based on the RGB color model.
    A particular color space that employs RGB primaries for part of its specification is defined by the three chromaticities of the red, green, and blue additive primaries,
    and can produce any chromaticity that is the 2D triangle defined by those primary colors (ie. excluding transfer function, white point, etc.).
    The primary colors are specified in terms of their CIE 1931 color space chromaticity coordinates (x,y), linking them to human-visible color.
    RGB is an abbreviation for red–green–blue.
    """

    def __init__(self, r: Decimal, g: Decimal, b: Decimal):
        assert r >= 0
        assert g >= 0
        assert b >= 0
        self.red = r
        self.green = g
        self.blue = b

    def to_rgb(self):
        return self

    def __deepcopy__(self, memodict={}):
        return RGBColor(self.red, self.green, self.blue)


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

    def __init__(self, c: Decimal, m: Decimal, y: Decimal, k: Decimal):
        self.cyan = c
        self.magenta = m
        self.yellow = y
        self.key = k

    def to_rgb(self) -> "RGBColor":
        ONE = Decimal(1)
        r = (ONE - self.cyan) * (ONE - self.key)
        g = (ONE - self.magenta) * (ONE - self.key)
        b = (ONE - self.yellow) * (ONE - self.key)
        return RGBColor(r, g, b)

    def __deepcopy__(self, memodict={}):
        return CMYKColor(self.cyan, self.magenta, self.yellow, self.key)


class GrayColor(Color):
    def __init__(self, g: Decimal):
        self.gray_level = g

    def to_rgb(self) -> "RGBColor":
        return RGBColor(self.gray_level, self.gray_level, self.gray_level)

    def __deepcopy__(self, memodict={}):
        return GrayColor(self.gray_level)


class HexColor(RGBColor):
    def __init__(self, hex_string: str):
        if hex_string.startswith("#"):
            hex_string = hex_string[1:]
        assert len(hex_string) == 6 or len(hex_string) == 8
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
        super(HexColor, self).__init__(Decimal(r), Decimal(g), Decimal(b))


class X11Color(HexColor):

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

    def __init__(self, color: str):
        assert color in X11Color.COLOR_DEFINITION
        super(X11Color, self).__init__(X11Color.COLOR_DEFINITION[color])
