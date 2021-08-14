import unittest
from decimal import Decimal

from borb.pdf.canvas.color.color import HexColor, HSVColor, RGBColor


class TestColorConversion(unittest.TestCase):
    @staticmethod
    def assert_is_almost(d0: Decimal, d1: Decimal):
        delta = abs(d0 - d1)
        assert delta <= Decimal(1)

    @staticmethod
    def assert_hsv_is_rgb(c0: HSVColor, c1: RGBColor):
        c2: RGBColor = c0.to_rgb()
        TestColorConversion.assert_is_almost(c2.red, c1.red)
        TestColorConversion.assert_is_almost(c2.green, c1.green)
        TestColorConversion.assert_is_almost(c2.blue, c1.blue)

    def test_hsv_to_rgb(self):

        # red
        TestColorConversion.assert_hsv_is_rgb(
            HSVColor(Decimal(0), Decimal(1), Decimal(1)),
            RGBColor(Decimal(1), Decimal(0), Decimal(0)),
        )

        # green
        TestColorConversion.assert_hsv_is_rgb(
            HSVColor(Decimal(120.0 / 360.0), Decimal(1), Decimal(1)),
            RGBColor(Decimal(0), Decimal(1), Decimal(0)),
        )

        # blue
        TestColorConversion.assert_hsv_is_rgb(
            HSVColor(Decimal(240.0 / 360.0), Decimal(1), Decimal(1)),
            RGBColor(Decimal(0), Decimal(0), Decimal(1)),
        )

    def test_hex_to_hsv(self):

        for hex_string in ["ACEB98", "87FF65", "A4C2A8", "5A5A66", "2A2B2E"]:
            c0 = HexColor(hex_string).to_rgb()
            c1 = HSVColor.from_rgb(c0)
            TestColorConversion.assert_hsv_is_rgb(c1, c0)
