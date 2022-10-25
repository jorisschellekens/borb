import unittest

from borb.io.read.types import Name


class TestNameBehaves_likeStr(unittest.TestCase):
    def test_name_behaves_like_str(self):

        d = {}
        d[Name("A")] = 1
        d[Name("B")] = 2
        d[Name("C")] = 3

        assert d["A"] == 1
