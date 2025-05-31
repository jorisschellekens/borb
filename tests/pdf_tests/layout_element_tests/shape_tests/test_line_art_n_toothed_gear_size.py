import unittest

from borb.pdf.layout_element.shape.line_art import LineArt


class TestLineArtNToothedGearSize(unittest.TestCase):

    def test_line_art_n_toothed_gear_003_size(self):
        w, h = LineArt.n_toothed_gear(n=3).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_toothed_gear_004_size(self):
        w, h = LineArt.n_toothed_gear(n=4).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_toothed_gear_005_size(self):
        w, h = LineArt.n_toothed_gear(n=5).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_toothed_gear_006_size(self):
        w, h = LineArt.n_toothed_gear(n=6).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_toothed_gear_007_size(self):
        w, h = LineArt.n_toothed_gear(n=7).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_toothed_gear_008_size(self):
        w, h = LineArt.n_toothed_gear(n=8).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_toothed_gear_009_size(self):
        w, h = LineArt.n_toothed_gear(n=9).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_toothed_gear_010_size(self):
        w, h = LineArt.n_toothed_gear(n=10).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
