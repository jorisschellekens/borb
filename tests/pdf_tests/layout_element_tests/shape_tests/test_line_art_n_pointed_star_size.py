import unittest

from borb.pdf.layout_element.shape.line_art import LineArt


class TestLineArtNPointedStarSize(unittest.TestCase):

    def test_line_art_n_pointed_star_size_003(self):
        w, h = LineArt.n_pointed_star(number_of_points=3).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_pointed_star_size_004(self):
        w, h = LineArt.n_pointed_star(number_of_points=4).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_pointed_star_size_005(self):
        w, h = LineArt.n_pointed_star(number_of_points=5).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_pointed_star_size_006(self):
        w, h = LineArt.n_pointed_star(number_of_points=6).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_pointed_star_size_007(self):
        w, h = LineArt.n_pointed_star(number_of_points=7).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_pointed_star_size_008(self):
        w, h = LineArt.n_pointed_star(number_of_points=8).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_pointed_star_size_009(self):
        w, h = LineArt.n_pointed_star(number_of_points=9).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]

    def test_line_art_n_pointed_star_size_010(self):
        w, h = LineArt.n_pointed_star(number_of_points=10).get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
