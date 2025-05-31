import unittest

from borb.pdf.layout_element.shape.map_of_north_america import MapOfNorthAmerica


class TestMapOfNorthAmericaSize(unittest.TestCase):

    def test_map_of_north_america_size(self):
        w, h = MapOfNorthAmerica().get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
