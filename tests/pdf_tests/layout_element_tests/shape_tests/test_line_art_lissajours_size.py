import unittest

from borb.pdf.layout_element.shape.line_art import LineArt


@unittest.skip
class TestLineArtLissajoursSize(unittest.TestCase):

    def test_line_art_lissajours_001_001_size(self):
        w, h = LineArt.lissajours(x_frequency=1, y_frequency=1).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_001_002_size(self):
        w, h = LineArt.lissajours(x_frequency=1, y_frequency=2).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_001_003_size(self):
        w, h = LineArt.lissajours(x_frequency=1, y_frequency=3).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_002_001_size(self):
        w, h = LineArt.lissajours(x_frequency=2, y_frequency=1).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_002_002_size(self):
        w, h = LineArt.lissajours(x_frequency=2, y_frequency=2).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_002_003_size(self):
        w, h = LineArt.lissajours(x_frequency=2, y_frequency=3).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_003_001_size(self):
        w, h = LineArt.lissajours(x_frequency=3, y_frequency=1).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_003_002_size(self):
        w, h = LineArt.lissajours(x_frequency=3, y_frequency=2).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_lissajours_003_003_size(self):
        w, h = LineArt.lissajours(x_frequency=3, y_frequency=3).get_size(
            available_space=(2**64, 2**64)
        )
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
