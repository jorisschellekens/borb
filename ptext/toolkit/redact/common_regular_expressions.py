#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class contains some useful (common) regular expressions.
"""
import re
from enum import Enum
from re import Pattern


class CommonRegularExpression(Enum):
    """
    This class contains some useful (common) regular expressions.
    """

    # fmt: off
    BITCOIN_ADDRESS: Pattern = re.compile("([13][a-km-zA-HJ-NP-Z0-9]{26,33})")
    EMAIL: Pattern = re.compile("(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}")
    IP_ADDRESS: Pattern = re.compile("\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b")
    ISBN_10: Pattern = re.compile("(97(8|9))?\d{9}(\d|X)")
    PHONE_NUMBER: Pattern = re.compile("[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*")
    ROMAN_NUMERAL: Pattern = re.compile("M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})")
    SOCIAL_SECURITY_NUMBER: Pattern = re.compile("\b(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})\b")
    # fmt: on
