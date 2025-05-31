import random
import unittest

from borb.pdf.layout_element.shape.line_art import LineArt


class TestLineArtBlobSize(unittest.TestCase):

    def test_line_art_blob_size(self):
        random.seed(0)
        w, h = LineArt.blob().get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
