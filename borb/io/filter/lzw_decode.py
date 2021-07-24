#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Decompresses data encoded using the LZW (Lempel-Ziv-Welch)
adaptive compression method, reproducing the original
text or binary data.
"""
import copy


class LZWDecode:
    """
    Decompresses data encoded using the LZW (Lempel-Ziv-
    Welch) adaptive compression method, reproducing the original
    text or binary data.
    """

    @staticmethod
    def decode(bytes_in: bytes) -> bytes:
        """
        Decompresses data encoded using the LZW (Lempel-Ziv-
        Welch) adaptive compression method
        """

        # trivial case
        if len(bytes_in) == 0:
            return bytes_in

        # Build the dictionary.
        dict_size = 256
        dictionary = {i: bytearray() for i in range(dict_size)}
        for k, v in dictionary.items():
            v.append(k)

        # use bytearray, otherwise this becomes O(N^2)
        # due to concatenation in a loop
        bytes_out = bytearray()
        w = bytearray()
        w.append(bytes_in[0])
        bytes_out.append(bytes_in[0])

        for i in range(1, len(bytes_in)):
            k = bytes_in[i]
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = copy.deepcopy(w)
                entry.append(w[0])
            else:
                assert False, "Unexpected error while performing LZW decode."
            bytes_out.extend(entry)

            # Add w+entry[0] to the dictionary.
            dictionary[dict_size] = copy.deepcopy(w)
            dictionary[dict_size].append(entry[0])
            dict_size += 1

            w = entry
        return bytes(bytes_out)
