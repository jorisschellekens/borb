#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Decompresses data encoded using a byte-oriented run-length
encoding algorithm, reproducing the original text or binary data
(typically monochrome image data, or any data that contains
frequent long runs of a single byte value).
"""
import logging

logger = logging.getLogger(__name__)


class RunLengthDecode:
    """
    Decompresses data encoded using a byte-oriented run-length
    encoding algorithm, reproducing the original text or binary data
    (typically monochrome image data, or any data that contains
    frequent long runs of a single byte value).
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def decode(bytes_in: bytes) -> bytes:
        """
        Decompresses data encoded using a byte-oriented run-length encoding algorithm
        :param bytes_in:    the input bytes
        :return:            the output bytes
        """

        # trivial case
        if len(bytes_in) == 0:
            return bytes_in

        # The RunLengthDecode filter decodes data that has been encoded in a simple byte-oriented format based on
        # run length. The encoded data shall be a sequence of runs, where each run shall consist of a length byte
        # followed by 1 to 128 bytes of data. If the length byte is in the range 0 to 127, the following length + 1 (1 to 128)
        # bytes shall be copied literally during decompression. If length is in the range 129 to 255, the following single
        # byte shall be copied 257 - length (2 to 128) times during decompression. A length value of 128 shall denote
        # EOF.
        bytes_out = bytearray()
        i: int = 0
        while i < len(bytes_in):
            b = bytes_in[i]
            # A length value of 128 shall denote EOF.
            if b == 128:
                break
            # If the length byte is in the range 0 to 127, the following length + 1 (1 to 128)
            # bytes shall be copied literally during decompression.
            length: int = 0
            if 0 <= b <= 127:
                length = b + 1
                i += 1
                for j in range(0, length):
                    bytes_out.append(bytes_in[i + j])
                i += length
                continue
            # If length is in the range 129 to 255, the following single
            # byte shall be copied 257 - length (2 to 128) times during decompression
            if 129 <= b <= 255:
                length = 257 - b
                i += 1
                for _ in range(0, length):
                    bytes_out.append(bytes_in[i])
                i += 1

        # return
        return bytes(bytes_out)
