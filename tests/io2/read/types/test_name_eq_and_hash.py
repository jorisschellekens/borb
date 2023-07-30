import unittest

from borb.io.read.types import Name


class TestNameEqAndHash(unittest.TestCase):
    """
    This test checks whether a borb Name object behaves like a str
    when used as a key in a dictionary.
    """

    def test_name_eq_and_hash(self):

        d = {}
        d[Name("A")] = 1
        d[Name("B")] = 2
        d[Name("C")] = 3

        assert d["A"] == 1
