import unittest
from decimal import Decimal

from borb.pdf import CMYKColor
from borb.pdf import Pantone
from borb.pdf.canvas.color.color import HSVColor
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.color.farrow_and_ball import FarrowAndBall


class TestColorConversion(unittest.TestCase):
    def test_rgb_to_cmyk(self):
        c0: RGBColor = RGBColor(Decimal(0.337), Decimal(0.796), Decimal(0.976))
        # to CMYK
        c1: CMYKColor = CMYKColor.from_rgb(c0)
        assert abs(c1.cyan - Decimal(0.655)) < Decimal(10 ** -3)
        assert abs(c1.magenta - Decimal(0.184)) < Decimal(10 ** -3)
        assert abs(c1.yellow - Decimal(0.000)) < Decimal(10 ** -3)
        assert abs(c1.key - Decimal(0.024)) < Decimal(10 ** -3)

        # back to RGB
        c2: RGBColor = c1.to_rgb()
        assert abs(c2.red - Decimal(0.337)) < Decimal(10 ** -3)
        assert abs(c2.green - Decimal(0.796)) < Decimal(10 ** -3)
        assert abs(c2.blue - Decimal(0.976)) < Decimal(10 ** -3)

    def test_rgb_to_farrow_and_ball(self):
        c0: RGBColor = RGBColor(Decimal(0.337), Decimal(0.796), Decimal(0.976))

        # to FarrowAndBall
        c1: FarrowAndBall = FarrowAndBall.find_nearest_farrow_and_ball_color(c0)
        assert c1.get_name() == "cooks-blue"
        assert abs(c1.red - Decimal(0.435)) < Decimal(10 ** -3)
        assert abs(c1.green - Decimal(0.580)) < Decimal(10 ** -3)
        assert abs(c1.blue - Decimal(0.702)) < Decimal(10 ** -3)

        # back to RGB
        c2: RGBColor = c1.to_rgb()
        assert abs(c2.red - Decimal(0.435)) < Decimal(10 ** -3)
        assert abs(c2.green - Decimal(0.580)) < Decimal(10 ** -3)
        assert abs(c2.blue - Decimal(0.702)) < Decimal(10 ** -3)

    # hex
    def test_rgb_to_hex_color(self):
        c0: RGBColor = RGBColor(Decimal(0.337), Decimal(0.796), Decimal(0.976))

        # to HexColor
        c1: HexColor = HexColor(c0.to_hex_string())
        assert c1.to_hex_string() == "#54c9f7"
        assert abs(c1.red - Decimal(0.333)) < Decimal(10 ** -3)
        assert abs(c1.green - Decimal(0.792)) < Decimal(10 ** -3)
        assert abs(c1.blue - Decimal(0.973)) < Decimal(10 ** -3)

        # to RGB
        c2: RGBColor = c1.to_rgb()
        assert abs(c2.red - Decimal(0.333)) < Decimal(10 ** -3)
        assert abs(c2.green - Decimal(0.792)) < Decimal(10 ** -3)
        assert abs(c2.blue - Decimal(0.973)) < Decimal(10 ** -3)

    # hsv
    def test_rgb_to_hsv(self):
        c0: RGBColor = RGBColor(Decimal(0.337), Decimal(0.796), Decimal(0.976))

        # to HSV
        c1: HSVColor = HSVColor.from_rgb(c0)
        assert abs(c1.hue - Decimal(0.547)) < Decimal(10 ** -3)
        assert abs(c1.saturation - Decimal(0.655)) < Decimal(10 ** -3)
        assert abs(c1.value - Decimal(0.976)) < Decimal(10 ** -3)

        # to RGB
        c2: RGBColor = c1.to_rgb()
        assert abs(c2.red - Decimal(0.337)) < Decimal(10 ** -3)
        assert abs(c2.green - Decimal(0.796)) < Decimal(10 ** -3)
        assert abs(c2.blue - Decimal(0.976)) < Decimal(10 ** -3)

    # pantone
    def test_rgb_to_pantone(self):
        c0: RGBColor = RGBColor(Decimal(0.337), Decimal(0.796), Decimal(0.976))

        # to FarrowAndBall
        c1: Pantone = Pantone.find_nearest_pantone_color(c0)
        assert c1.get_name() == "blue-radiance"
        assert abs(c1.red - Decimal(0.345)) < Decimal(10 ** -3)
        assert abs(c1.green - Decimal(0.788)) < Decimal(10 ** -3)
        assert abs(c1.blue - Decimal(0.831)) < Decimal(10 ** -3)

        # back to RGB
        c2: RGBColor = c1.to_rgb()
        assert abs(c2.red - Decimal(0.345)) < Decimal(10 ** -3)
        assert abs(c2.green - Decimal(0.788)) < Decimal(10 ** -3)
        assert abs(c2.blue - Decimal(0.831)) < Decimal(10 ** -3)
