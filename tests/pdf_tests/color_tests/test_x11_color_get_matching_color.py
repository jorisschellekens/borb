import unittest

from borb.pdf.color.x11_color import X11Color


class TestX11ColorGetMatchingColor(unittest.TestCase):

    def test_x11_color_get_matching_color_000(self):
        assert X11Color.get_matching_color(X11Color.ALICE_BLUE)[0] == "ALICE_BLUE"

    def test_x11_color_get_matching_color_001(self):
        assert X11Color.get_matching_color(X11Color.BEIGE)[0] == "BEIGE"

    def test_x11_color_get_matching_color_002(self):
        assert X11Color.get_matching_color(X11Color.CADET_BLUE)[0] == "CADET_BLUE"

    def test_x11_color_get_matching_color_003(self):
        assert X11Color.get_matching_color(X11Color.DARK_BLUE)[0] == "DARK_BLUE"

    def test_x11_color_get_matching_color_004(self):
        assert X11Color.get_matching_color(X11Color.FIREBRICK)[0] == "FIREBRICK"

    def test_x11_color_get_matching_color_005(self):
        assert X11Color.get_matching_color(X11Color.GAINSBORO)[0] == "GAINSBORO"

    def test_x11_color_get_matching_color_006(self):
        assert X11Color.get_matching_color(X11Color.HONEYDEW)[0] == "HONEYDEW"

    def test_x11_color_get_matching_color_007(self):
        assert X11Color.get_matching_color(X11Color.INDIAN_RED)[0] == "INDIAN_RED"

    def test_x11_color_get_matching_color_008(self):
        assert X11Color.get_matching_color(X11Color.KHAKI)[0] == "KHAKI"

    def test_x11_color_get_matching_color_009(self):
        assert X11Color.get_matching_color(X11Color.LAVENDER)[0] == "LAVENDER"
