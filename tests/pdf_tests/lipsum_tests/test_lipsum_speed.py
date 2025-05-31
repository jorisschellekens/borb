import time
import typing
import unittest

from borb.pdf.lipsum.lipsum import Lipsum


class TestLipsumSpeed(unittest.TestCase):

    def test_lipsum_agatha_christie_speed(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                delta: float = time.time()
                s = Lipsum.generate_agatha_christie(n)
                delta = time.time() - delta
                l += [(delta, len(s))]
            avg_speed_per_char = sum([x / y for x, y in l]) / len(l)
            assert avg_speed_per_char < 0.0001

    def test_lipsum_arthur_conan_doyle_speed(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                delta: float = time.time()
                s = Lipsum.generate_arthur_conan_doyle(n)
                delta = time.time() - delta
                l += [(delta, len(s))]
            avg_speed_per_char = sum([x / y for x, y in l]) / len(l)
            assert avg_speed_per_char < 0.0001

    def test_lipsum_jane_austen_speed(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                delta: float = time.time()
                s = Lipsum.generate_jane_austen(n)
                delta = time.time() - delta
                l += [(delta, len(s))]
            avg_speed_per_char = sum([x / y for x, y in l]) / len(l)
            assert avg_speed_per_char < 0.0001

    def test_lipsum_lorem_ipsum_speed(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                delta: float = time.time()
                s = Lipsum.generate_lorem_ipsum(n)
                delta = time.time() - delta
                l += [(delta, len(s))]
            avg_speed_per_char = sum([x / y for x, y in l]) / len(l)
            assert avg_speed_per_char < 0.0001

    def test_lipsum_mary_shelley_speed(self):
        for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            l: typing.List[int] = []
            for _ in range(0, 100):
                delta: float = time.time()
                s = Lipsum.generate_mary_shelley(n)
                delta = time.time() - delta
                l += [(delta, len(s))]
            avg_speed_per_char = sum([x / y for x, y in l]) / len(l)
            assert avg_speed_per_char < 0.0001
