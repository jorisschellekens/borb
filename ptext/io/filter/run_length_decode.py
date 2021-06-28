#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Decompresses data encoded using a byte-oriented run-length
encoding algorithm, reproducing the original text or binary data
(typically monochrome image data, or any data that contains
frequent long runs of a single byte value).
"""


class RunLengthDecode:
    """
    Decompresses data encoded using a byte-oriented run-length
    encoding algorithm, reproducing the original text or binary data
    (typically monochrome image data, or any data that contains
    frequent long runs of a single byte value).
    """

    @staticmethod
    def decode(bytes_in: bytes) -> bytes:
        """
        Decompresses data encoded using a byte-oriented run-length
        encoding algorithm
        """

        # trivial case
        if len(bytes_in) == 0:
            return bytes_in

        bytes_out = bytearray()
        for i in range(0, len(bytes_in), 2):
            b = bytes_in[i]
            n = bytes_in[i + 1]
            for j in range(0, n):
                bytes_out.append(b)

        return bytes(bytes_out)
