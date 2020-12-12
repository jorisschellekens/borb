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

    def to_rgb(self) -> "Color":
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

    def to_rgb(self) -> "Color":
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

    def to_rgb(self) -> "Color":
        return RGBColor(self.gray_level, self.gray_level, self.gray_level)

    def __deepcopy__(self, memodict={}):
        return GrayColor(self.gray_level)
