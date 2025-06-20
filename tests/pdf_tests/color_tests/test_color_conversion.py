import unittest

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color


class TestColorConversion(unittest.TestCase):

    def test_color_conversion(self):
        c0: Color = X11Color.YELLOW_MUNSELL

        # --> RGB
        c1: Color = c0.to_rgb_color()

        # --> HSV
        c2: Color = c1.to_hsv_color()

        # --> RGB
        c3: Color = c2.to_rgb_color()

        print(f"{c0.to_hex_str()} --> {c3.to_hex_str()}")
