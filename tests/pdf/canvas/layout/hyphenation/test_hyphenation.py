import unittest

from borb.datastructure.str_trie import Trie
from borb.pdf.canvas.layout.hyphenation.hyphenation import (
    Hyphenation,
)


class TestHyphenation(unittest.TestCase):
    def test_hyphenation_af_001(self):
        h = Hyphenation("af")
        assert h.hyphenate("dokter", "-") == "dok-ter"
        assert h.hyphenate("marginaal", "-") == "mar-gi-naal"
        assert h.hyphenate("sandaal", "-") == "sandaal"

    def test_hyphenation_en_gb_001(self):
        h = Hyphenation("en-gb")
        assert h.hyphenate("astute", "-") in ["astute", "as-tute"]
        assert h.hyphenate("birmingham", "-") == "birm-ing-ham"
        assert h.hyphenate("crab", "-") == "crab"

    def test_hyphenation_en_gb_002(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happen
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 0
        Hyphenation.DO_NOT_HYPHENATE_AFTER = 0
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "a-a-a-a-a-a-a"

    def test_hyphenation_en_gb_003(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happend
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 1
        Hyphenation.DO_NOT_HYPHENATE_AFTER = 32
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "aa-a-a-a-a-a"

    def test_hyphenation_en_gb_004(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happend
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 0
        Hyphenation.DO_NOT_HYPHENATE_AFTER = -1
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "a-a-a-a-a-aa"

    def test_hyphenation_en_gb_005(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happend
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 1
        Hyphenation.DO_NOT_HYPHENATE_AFTER = -1
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "aa-a-a-a-aa"
