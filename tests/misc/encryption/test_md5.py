import typing
import unittest
from hashlib import md5


class TestMD5(unittest.TestCase):
    def test_md5(self):
        # fmt: off
        raw_input: bytes = bytes([40, 191, 78, 94, 78, 117, 138, 65,
                                  100, 0, 78, 86, 255, 250, 1, 8,
                                  46, 46, 0, 182, 208, 104, 62, 128,
                                  47, 12, 169, 254, 100, 83, 105, 122])
        # fmt: on

        # construct hashing algorithm
        h = md5()

        # update
        h.update(raw_input)

        # get hash
        raw_output: typing.List[int] = [
            (x - 256) if x >= 128 else x for x in h.digest()
        ]

        # assert
        assert raw_output == [
            81,
            33,
            71,
            -71,
            -98,
            113,
            -27,
            117,
            120,
            7,
            121,
            -95,
            -74,
            69,
            20,
            72,
        ]

    def test_md5_50(self):
        # fmt: off
        raw_input: bytes = bytes([40, 191, 78, 94, 78, 117, 138, 65,
                                  100, 0, 78, 86, 255, 250, 1, 8,
                                  46, 46, 0, 182, 208, 104, 62, 128,
                                  47, 12, 169, 254, 100, 83, 105, 122])
        # fmt: on

        # construct hashing algorithm
        h = md5()

        h.update(raw_input)
        raw_output: typing.List[int] = [
            (x - 256) if x >= 128 else x for x in h.digest()
        ]
        assert raw_output == [
            81,
            33,
            71,
            -71,
            -98,
            113,
            -27,
            117,
            120,
            7,
            121,
            -95,
            -74,
            69,
            20,
            72,
        ]

        # 50 iterations
        prev: bytes = h.digest()
        for _ in range(0, 50):
            h = md5()
            h.update(prev)
            prev = h.digest()[0:16]

        # assert
        raw_output: typing.List[int] = [(x - 256) if x >= 128 else x for x in prev]
        assert raw_output == [
            90,
            0,
            52,
            79,
            64,
            -48,
            -91,
            -59,
            43,
            22,
            11,
            -125,
            14,
            110,
            8,
            110,
        ]
