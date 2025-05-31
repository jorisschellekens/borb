import typing
import unittest

from borb.pdf.lipsum.lipsum import Lipsum


class TestLipsumLength(unittest.TestCase):

    def test_lipsum_agatha_christie_length(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                l += [len(Lipsum.generate_agatha_christie(n=n))]
            nof_good_sentences: int = sum(
                [1 if (n - 5) <= x <= (n + 5) else 0 for x in l]
            )
            assert nof_good_sentences / len(l) >= 0.80

    def test_lipsum_arthur_conan_doyle_length(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                l += [len(Lipsum.generate_arthur_conan_doyle(n=n))]
            nof_good_sentences: int = sum(
                [1 if (n - 5) <= x <= (n + 5) else 0 for x in l]
            )
            assert nof_good_sentences / len(l) >= 0.80

    def test_lipsum_jane_austen_length(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                l += [len(Lipsum.generate_jane_austen(n=n))]
            nof_good_sentences: int = sum(
                [1 if (n - 5) <= x <= (n + 5) else 0 for x in l]
            )
            assert nof_good_sentences / len(l) >= 0.80

    def test_lipsum_lorem_ipsum_length(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                l += [len(Lipsum.generate_lorem_ipsum(n=n))]
            nof_good_sentences: int = sum(
                [1 if (n - 5) <= x <= (n + 5) else 0 for x in l]
            )
            assert nof_good_sentences / len(l) >= 0.80

    def test_lipsum_mary_shelley_length(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                l += [len(Lipsum.generate_mary_shelley(n=n))]
            nof_good_sentences: int = sum(
                [1 if (n - 5) <= x <= (n + 5) else 0 for x in l]
            )
            assert nof_good_sentences / len(l) >= 0.80
