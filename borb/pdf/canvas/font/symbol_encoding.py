#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In PDF, a font is classified as either nonsymbolic or symbolic according to whether all of its characters are
members of the standard Latin character set; see D.2, “Latin Character Set and Encodings”. This shall be
indicated by flags in the font descriptor; see 9.8.2, "Font Descriptor Flags". Symbolic fonts contain other
character sets, to which the encodings mentioned previously ordinarily do not apply. Such font programs have
built-in encodings that are usually unique to each font. The standard 14 fonts include two symbolic fonts,
Symbol and ZapfDingbats, whose encodings and character sets are documented in Annex D.
"""

# fmt: off
SYMBOL_ENCODING_LOOKUP = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    32, 33, 8704, 35, 8707, 37, 38, 8715,
    40, 41, 42, 43, 44, 45, 46, 47,
    48, 49, 50, 51, 52, 53, 54, 55,
    56, 57, 58, 59, 60, 61, 62, 63,
    8773, 913, 914, 935, 916, 917, 934, 915,
    919, 921, 977, 922, 923, 924, 925, 927,
    928, 920, 929, 931, 932, 933, 962, 937,
    926, 936, 918, 91, 8756, 93, 8869, 95,
    773, 945, 946, 967, 948, 949, 981, 947,
    951, 953, 966, 954, 955, 956, 957, 959,
    960, 952, 961, 963, 964, 965, 982, 969,
    958, 968, 950, 123, 124, 125, 126, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    8364, 978, 8242, 8804, 8260, 8734, 402, 9827,
    9830, 9829, 9824, 8596, 8592, 8593, 8594, 8595,
    176, 177, 8243, 8805, 215, 8733, 8706, 8226,
    247, 8800, 8801, 8776, 8230, 9474, 9472, 8629,
    8501, 8465, 8476, 8472, 8855, 8853, 8709, 8745,
    8746, 8835, 8839, 8836, 8834, 8838, 8712, 8713,
    8736, 8711, 174, 169, 8482, 8719, 8730, 8901,
    172, 8743, 8744, 8660, 8656, 8657, 8658, 8659,
    9674, 9001, 0, 0, 0, 8721, 9115, 9116,
    9117, 9121, 9122, 9123, 9127, 9128, 9129, 9130,
    0, 9002, 8747, 8992, 9134, 8993, 9118, 9119,
    9120, 9124, 9125, 9126, 9131, 9132, 9133, 0,
]
# fmt: on


def symbol_decode(byte_input: bytes) -> str:
    """
    This function decodes bytes using SymbolEncoding
    :param byte_input:  the input
    :return:            a str (representing the decoded bytes)
    """
    s: str = ""
    for b in byte_input:
        s += chr(SYMBOL_ENCODING_LOOKUP[b])
    return s


def symbol_encode(str_input: str) -> bytes:
    """
    This function encodes a str using SymbolEncoding
    :param str_input:   the input
    :return:            bytes (representing the encoded str)
    """
    b: bytearray = bytearray()
    for c in str_input:
        char_index: int = -1
        try:
            char_index = SYMBOL_ENCODING_LOOKUP.index(ord(c))
        except ValueError:
            pass
        if char_index != -1:
            b.append(char_index)
    return b


# fmt: off
ZAPFDINGBATS_ENCODING_LOOKUP = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    32, 9985, 9986, 9987, 9988, 9742, 9990, 9991,
    9992, 9993, 9755, 9758, 9996, 9997, 9998, 9999,
    10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007,
    10008, 10009, 10010, 10011, 10012, 10013, 10014, 10015,
    10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023,
    9733, 10025, 10026, 10027, 10028, 10029, 10030, 10031,
    10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039,
    10040, 10041, 10042, 10043, 10044, 10045, 10046, 10047,
    10048, 10049, 10050, 10051, 10052, 10053, 10054, 10055,
    10056, 10057, 10058, 10059, 9679, 10061, 9632, 10063,
    10064, 10065, 10066, 9650, 9660, 9670, 10070, 9687,
    10072, 10073, 10074, 10075, 10076, 10077, 10078, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 10081, 10082, 10083, 10084, 10085, 10086, 10087,
    9827, 9830, 9829, 9824, 9312, 9313, 9314, 9315,
    9316, 9317, 9318, 9319, 9320, 9321, 10102, 10103,
    10104, 10105, 10106, 10107, 10108, 10109, 10110, 10111,
    10112, 10113, 10114, 10115, 10116, 10117, 10118, 10119,
    10120, 10121, 10122, 10123, 10124, 10125, 10126, 10127,
    10128, 10129, 10130, 10131, 10132, 8594, 8596, 8597,
    10136, 10137, 10138, 10139, 10140, 10141, 10142, 10143,
    10144, 10145, 10146, 10147, 10148, 10149, 10150, 10151,
    10152, 10153, 10154, 10155, 10156, 10157, 10158, 10159,
    0, 10161, 10162, 10163, 10164, 10165, 10166, 10167,
    10168, 10169, 10170, 10171, 10172, 10173, 10174, 0,
]
# fmt: on


def zapfdingbats_decode(byte_input: bytes) -> str:
    """
    This function decodes bytes using ZapfDingbats
    :param byte_input:  the input
    :return:            a str (representing the decoded bytes)
    """
    s: str = ""
    for b in byte_input:
        s += chr(ZAPFDINGBATS_ENCODING_LOOKUP[b])
    return s


def zapfdingbats_encode(str_input: str) -> bytes:
    """
    This function encodes a str using ZapfDingbats
    :param str_input:   the input
    :return:            bytes (representing the encoded str)
    """
    b: bytearray = bytearray()
    for c in str_input:
        char_index: int = -1
        try:
            char_index = ZAPFDINGBATS_ENCODING_LOOKUP.index(ord(c))
        except ValueError:
            pass
        if char_index != -1:
            b.append(char_index)
    return b
