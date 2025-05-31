import unittest

from borb.pdf.layout_element.shape.map_of_africa import MapOfAfrica


class TestMapOfAfricaSize(unittest.TestCase):

    def test_map_of_africa_size(self):
        w, h = MapOfAfrica().get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
