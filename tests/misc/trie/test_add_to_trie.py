import unittest

from borb.datastructure.str_trie import Trie


class TestAddToTrie(unittest.TestCase):
    def test_add_to_trie(self):
        t = Trie()

        t["lorem"] = 2
        t["ipsum"] = 3
        t["dolor"] = 5
        t["sit"] = 7
        t["amet"] = 11
        t["consectetur"] = 13
        t["adipiscing"] = 17
        t["elit"] = 19
        t["sed"] = 23
        t["do"] = 29
        t["eiusmod"] = 31

        assert len(t) == 11

        assert t["lorem"] == 2
        assert t["ipsum"] == 3
        assert t["dolor"] == 5
        assert t["sit"] == 7
        assert t["amet"] == 11
        assert t["consectetur"] == 13
        assert t["adipiscing"] == 17
        assert t["elit"] == 19
        assert t["sed"] == 23
        assert t["do"] == 29
        assert t["eiusmod"] == 31
