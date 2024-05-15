#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
One commonly used font encoding for Latin-text font programs is often referred to as StandardEncoding or
sometimes as the Adobe standard encoding. The name StandardEncoding shall have no special meaning in
PDF, but this encoding does play a role as a default encoding (as shown in Table 114).

This is the built-in encoding defined in Type 1 Latin-text font programs (but generally not in TrueType font
programs). Conforming readers shall not have a predefined encoding named StandardEncoding. However, it is necessary to describe this
encoding, since a font’s built-in encoding can be used as the base encoding from which differences may be specified in an encoding
dictionary.
"""

# fmt: off
ADOBE_STANDARD_ENCODING_LOOKUP = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    32, 33, 34, 35, 36, 37, 38, 39,
    40, 41, 42, 43, 44, 45, 46, 47,
    48, 49, 50, 51, 52, 53, 54, 55,
    56, 57, 58, 59, 60, 61, 62, 63,
    64, 65, 66, 67, 68, 69, 70, 71,
    72, 73, 74, 75, 76, 77, 78, 79,
    80, 81, 82, 83, 84, 85, 86, 87,
    88, 89, 90, 91, 92, 93, 94, 95,
    8216, 97, 98, 99, 100, 101, 102, 103,
    104, 105, 106, 107, 108, 109, 110, 111,
    112, 113, 114, 115, 116, 117, 118, 119,
    120, 121, 122, 123, 124, 125, 126, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 161, 162, 163, 8260, 165, 402, 167,
    164, 39, 8220, 171, 8249, 8250, 64257, 64258,
    0, 8211, 8224, 8225, 183, 0, 182, 8226,
    8218, 8222, 8221, 187, 8230, 8240, 0, 191,
    0, 96, 180, 710, 732, 175, 728, 729,
    168, 0, 730, 184, 0, 733, 731, 711,
    8212, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 198, 0, 170, 0, 0, 0, 0,
    321, 216, 338, 186, 0, 0, 0, 0,
    0, 230, 0, 0, 0, 305, 0, 0,
    322, 248, 339, 223, 0, 0, 0, 0,
]
# fmt: on


def adobe_standard_decode(byte_input: bytes) -> str:
    """
    This function decodes bytes using StandardEncoding
    :param byte_input:  the input
    :return:            a str (representing the decoded bytes)
    """
    s: str = ""
    for b in byte_input:
        s += chr(ADOBE_STANDARD_ENCODING_LOOKUP[b])
    return s


def adobe_standard_encode(str_input: str) -> bytes:
    """
    This function encodes a str using StandardEncoding
    :param str_input:   the input
    :return:            bytes (representing the encoded str)
    """
    b: bytearray = bytearray()
    for c in str_input:
        char_index: int = -1
        try:
            char_index = ADOBE_STANDARD_ENCODING_LOOKUP.index(ord(c))
        except ValueError:
            pass
        if char_index != -1:
            b.append(char_index)
    return b
