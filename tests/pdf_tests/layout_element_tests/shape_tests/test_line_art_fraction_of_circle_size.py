import unittest

from borb.pdf.layout_element.shape.line_art import LineArt


class TestLineArtFractionOfCircleSize(unittest.TestCase):

    def test_line_art_fraction_of_circle_060(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=60).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_090(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=90).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_120(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=120).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_150(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=150).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_180(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=180).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_210(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=210).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_240(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=240).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_270(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=270).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_300(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=300).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_330(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=330).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_fraction_of_circle_360(self):
        w, h = LineArt.fraction_of_circle(angle_in_degrees=360).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
