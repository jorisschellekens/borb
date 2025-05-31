#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class to handle LZW (Lempel-Ziv-Welch) compression decoding in the context of PDF data.

LZW is a lossless data compression algorithm that is used in various contexts, including PDF image
compression. This class provides functionality to decode data that has been compressed using LZW,
which is commonly used for handling image data and other compressed content in a PDF file.

The decoding process involves reversing the LZW encoding algorithm to restore the original, uncompressed
data from the encoded byte sequence. This class can be used for handling compressed data streams
within a PDF document, including but not limited to image streams, object data, and other binary content.
"""
import typing


class bitarray:
    """
    A class for working with a byte sequence and retrieving individual bits.

    This class provides functionality for interpreting a sequence of bytes as a series of bits.
    It allows you to extract individual bits (as integers) from a byte sequence, enabling efficient bit-level operations
    commonly needed in algorithms such as compression, encoding, and cryptography.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, input: bytes):
        """
        Initialize an instance of the class with the provided byte input.

        This constructor sets up an internal buffer and other variables to handle the processing
        of the byte sequence (`input`). It prepares the object to manage and manipulate the byte
        stream in subsequent operations.

        :param input:   The input byte sequence to be processed.
                        This is typically raw data to be manipulated, decoded, or analyzed within the class.
        """
        self._buffer: typing.List[int] = []
        self._default_to_return: int = 256
        self._pos: int = -1
        self._src: bytes = input

    #
    # PRIVATE
    #

    def __read_next_byte(self):
        self._pos += 1
        self._buffer += [int(x) for x in "{0:08b}".format(self._src[self._pos])]

    #
    # PUBLIC
    #

    def next(self, n: int) -> int:
        """
        Read the next `n` bits from the input and returns them as an integer.

        This method retrieves the specified number of bits from the current position
        in the bit stream. If the internal buffer does not contain enough bits,
        additional bytes are read from the source to ensure `n` bits are available.
        The retrieved bits are then removed from the buffer.

        :param n:   The number of bits to retrieve.
        :return:    The next `n` bits from the input, represented as an integer.
                    If there are not enough bits, the method returns a default value.

        :raises ValueError: If the input contains invalid binary data that cannot be processed.
        """
        try:
            while n > len(self._buffer):
                self.__read_next_byte()
            x: typing.List[int] = self._buffer[:n]
            self._buffer = self._buffer[n:]
            return int("".join([str(y) for y in x]), 2)
        except:
            return self._default_to_return


class LZWDecode:
    """
    A class to handle LZW (Lempel-Ziv-Welch) compression decoding in the context of PDF data.

    LZW is a lossless data compression algorithm that is used in various contexts, including PDF image
    compression. This class provides functionality to decode data that has been compressed using LZW,
    which is commonly used for handling image data and other compressed content in a PDF file.

    The decoding process involves reversing the LZW encoding algorithm to restore the original, uncompressed
    data from the encoded byte sequence. This class can be used for handling compressed data streams
    within a PDF document, including but not limited to image streams, object data, and other binary content.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize an instance of the LZWDecode class, setting up the initial state for decoding.

        This constructor sets the necessary attributes required for decoding LZW-compressed data:
        - `_bits_to_read`: The number of bits to read for each LZW code (typically 9 bits initially).
        - `_lookup_table`: A dictionary that will be used as a lookup table to store the LZW codes and their corresponding byte sequences.
        - `_table_index`: The current index used to track the next available LZW code in the lookup table.

        These attributes are critical for the LZW decoding process, where the lookup table is progressively built
        as new codes are encountered during decoding, and the number of bits used to read codes may increase as
        more dictionary entries are added.

        This setup prepares the instance to begin decoding a byte stream that has been encoded using the LZW algorithm.
        """
        self._bits_to_read: int = 9  # type: ignore[annotation-unchecked]
        self._lookup_table: typing.Dict[int, bytearray] = {}  # type: ignore[annotation-unchecked]
        self._table_index: int = 0  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    def __add_to_lookup_table(self, new_bytes: bytes, prev_bytes: bytearray):
        self._lookup_table[self._table_index] = prev_bytes + new_bytes
        self._table_index += 1
        if self._table_index == 511:
            self._bits_to_read = 10
        elif self._table_index == 1023:
            self._bits_to_read = 11
        elif self._table_index == 2047:
            self._bits_to_read = 12

    def __init_lookup_table(self):
        self._lookup_table = {i: i.to_bytes(1, "big") for i in range(0, 256)}
        self._table_index = 258
        self._bits_to_read = 9

    #
    # PUBLIC
    #

    def decode(self, input: bytes):
        """
        Decode data compressed using the LZW algorithm.

        This method reverses the LZW compression algorithm, transforming a compressed byte stream back into
        its original, uncompressed form. LZW (Lempel-Ziv-Welch) is a lossless compression algorithm widely
        used in PDF for compressing image and data streams. It uses a dictionary-based approach to replace
        repetitive patterns in the data with shorter codes.

        :param bytes_in: The LZW-compressed byte sequence that will be decoded.
        :return: The decompressed byte sequence after applying the LZW algorithm to the input data.
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
                self.__init_lookup_table()
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
                self.__add_to_lookup_table(
                    new_bytes=x[0:1], prev_bytes=self._lookup_table[prev_code]
                )
                prev_code = code
            else:
                x = self._lookup_table[prev_code]
                x = x + x[0:1]
                bytes_out += x
                self.__add_to_lookup_table(new_bytes=bytearray(), prev_bytes=x)
                prev_code = code

        # return bytes
        return bytes_out
