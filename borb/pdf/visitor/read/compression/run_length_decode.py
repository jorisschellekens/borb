#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Decompresses data encoded using a byte-oriented run-length encoding (RLE) algorithm.

Run-Length Encoding (RLE) is a simple data compression technique that replaces sequences
of the same data value (or byte) occurring in consecutive data elements (runs) with a
single value and a count. This class provides the functionality to decode such compressed
data back into its original form.

RLE is commonly used in scenarios where data has repeated values, such as in monochrome
image compression or certain types of text and binary data.

The algorithm identifies runs of the same byte value and decompresses them by repeating
the byte for the specified number of times, thus reproducing the original data.
"""
import logging

logger = logging.getLogger(__name__)


class RunLengthDecode:
    """
    Decompresses data encoded using a byte-oriented run-length encoding (RLE) algorithm.

    Run-Length Encoding (RLE) is a simple data compression technique that replaces sequences
    of the same data value (or byte) occurring in consecutive data elements (runs) with a
    single value and a count. This class provides the functionality to decode such compressed
    data back into its original form.

    RLE is commonly used in scenarios where data has repeated values, such as in monochrome
    image compression or certain types of text and binary data.

    The algorithm identifies runs of the same byte value and decompresses them by repeating
    the byte for the specified number of times, thus reproducing the original data.
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
        Decompress data encoded using a byte-oriented run-length encoding (RLE) algorithm.

        This method decodes data that was compressed using the RLE technique, where sequences
        of identical bytes are replaced with a single byte value followed by a repetition count.
        During decompression, each encoded sequence is expanded back to its original repeated form.

        The RLE encoding typically follows this format:
        - A length byte `n` is followed by a data byte `b`.
          - If `0 <= n <= 127`, it represents `n + 1` literal bytes (not compressed).
          - If `129 <= n <= 255`, it represents a repeated sequence of `257 - n` instances of `b`.
          - A special marker value `128` may signal the end of the compressed data.

        :param bytes_in:    The input bytes compressed using run-length encoding.
        :return:            The decompressed output bytes.
        :raises ValueError: If the input contains invalid RLE data.
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
