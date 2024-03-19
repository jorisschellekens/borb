#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Decompresses data encoded using the LZW (Lempel-Ziv-Welch) adaptive compression method,
reproducing the original text or binary data.
"""
import typing


class bitarray:
    """
    This class works allows you to work with a bytes input
    and retrieve individual bits (as integers)
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, input: bytes):
        self._buffer: typing.List[int] = []
        self._default_to_return: int = 256
        self._pos: int = -1
        self._src: bytes = input

    #
    # PRIVATE
    #

    def _read_next_byte(self):
        self._pos += 1
        self._buffer += [int(x) for x in "{0:08b}".format(self._src[self._pos])]

    #
    # PUBLIC
    #

    def next(self, n) -> int:
        """
        This function reads the next n bits from the input
        :param n:   the number of bits to retrieve
        :return:    the next n bits from the input as an integer
        """
        try:
            while n > len(self._buffer):
                self._read_next_byte()
            x: typing.List[int] = self._buffer[:n]
            self._buffer = self._buffer[n:]
            return int("".join([str(y) for y in x]), 2)
        except:
            return self._default_to_return


class LZWDecode:
    """
    Decompresses data encoded using the LZW (Lempel-Ziv-Welch) adaptive compression method,
    reproducing the original text or binary data.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._bits_to_read: int = 9
        self._lookup_table: typing.Dict[int, bytearray] = {}
        self._table_index: int = 0

    #
    # PRIVATE
    #

    def _add_to_lookup_table(self, new_bytes: bytes, prev_bytes: bytearray):
        self._lookup_table[self._table_index] = prev_bytes + new_bytes
        self._table_index += 1
        if self._table_index == 511:
            self._bits_to_read = 10
        elif self._table_index == 1023:
            self._bits_to_read = 11
        elif self._table_index == 2047:
            self._bits_to_read = 12

    def _init_lookup_table(self):
        self._lookup_table = {i: i.to_bytes(1, "big") for i in range(0, 256)}
        self._table_index = 258
        self._bits_to_read = 9

    #
    # PUBLIC
    #

    def decode(self, input: bytes):
        """
        Decompresses data encoded using the LZW (Lempel-Ziv-Welch) adaptive compression method
        :param input:   the input bytes
        :return:        the output bytes
        """

        # output
        bytes_out: bytearray = bytearray()

        # read
        bit_input: bitarray = bitarray(input)
        prev_code: int = 0
        code: int = 0

        while code != 257:
            code = bit_input.next(self._bits_to_read)
            if code == 257:
                break

            # init
            if code == 256:
                self._init_lookup_table()
                code = bit_input.next(self._bits_to_read)
                if code == 257:
                    break
                bytes_out += self._lookup_table[code]
                prev_code = code
                continue

            # normal behaviour
            x: bytearray = bytearray()
            if code < self._table_index:
                x = self._lookup_table[code]
                bytes_out += x
                self._add_to_lookup_table(
                    new_bytes=x[0:1], prev_bytes=self._lookup_table[prev_code]
                )
                prev_code = code
            else:
                x = self._lookup_table[prev_code]
                x = x + x[0:1]
                bytes_out += x
                self._add_to_lookup_table(new_bytes=bytearray(), prev_bytes=x)
                prev_code = code

        # return bytes
        return bytes_out
