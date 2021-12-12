import unittest

from borb.pdf.canvas.layout.hyphenation.hyphenation import (
    Hyphenation,
)


class TestHyphenation(unittest.TestCase):
    def test_hyphenation_af(self):
        h = Hyphenation("af")
        assert h.hyphenate("dokter", "-") == "dok-ter"
        assert h.hyphenate("marginaal", "-") == "mar-gi-naal"
        assert h.hyphenate("sandaal", "-") == "sandaal"

    def test_hyphenation_en_gb(self):
        h = Hyphenation("en-gb")
        assert h.hyphenate("astute", "-") == "as-tute"
        assert h.hyphenate("birmingham", "-") == "birm-ing-ham"
        assert h.hyphenate("crab", "-") == "crab"
