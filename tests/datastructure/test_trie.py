import unittest

from borb.datastructure.str_trie import Trie


class TestTrie(unittest.TestCase):
    """
    This test checks some of the functionalities of the Trie datastructure.
    Tries are used in the hyphenation algorithm.
    """

    def test_trie_len(self):

        # init
        t = Trie()

        # insert
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

        # check length
        assert len(t) == 11

    def test_trie_getitem(self):

        # init
        t = Trie()

        # insert
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

        # check __getitem__
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
