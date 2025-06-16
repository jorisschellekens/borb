import unittest

from borb.pdf.layout_element.shape.line_art import LineArt


class TestLineArtNGonSize(unittest.TestCase):

    def test_line_art_n_gon_size_003_size(self):
        w, h = LineArt.n_gon(number_of_sides=3).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_gon_size_004_size(self):
        w, h = LineArt.n_gon(number_of_sides=4).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_gon_size_005_size(self):
        w, h = LineArt.n_gon(number_of_sides=5).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_gon_size_006_size(self):
        w, h = LineArt.n_gon(number_of_sides=6).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_gon_size_007_size(self):
        w, h = LineArt.n_gon(number_of_sides=7).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_gon_size_008_size(self):
        w, h = LineArt.n_gon(number_of_sides=8).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_gon_size_009_size(self):
        w, h = LineArt.n_gon(number_of_sides=9).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_gon_size_010_size(self):
        w, h = LineArt.n_gon(number_of_sides=10).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
