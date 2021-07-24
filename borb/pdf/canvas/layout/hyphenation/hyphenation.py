#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Syllabification or syllabication, also known as hyphenation, is the separation of a word into syllables, whether spoken, written or signed.
A hyphenation algorithm is a set of rules, especially one codified for implementation in a computer program,
that decides at which points a word can be broken over two lines with a hyphen.
For example, a hyphenation algorithm might decide that impeachment can be broken as impeach-ment or im-peachment but not impe-achment.
One of the reasons for the complexity of the rules of word-breaking is that different "dialects" of English tend to differ on hyphenation[citation needed]:
American English tends to work on sound,
but British English tends to look to the origins of the word and then to sound.
There are also a large number of exceptions, which further complicates matters.
"""
import json
import typing
from pathlib import Path

from borb.datastructure.str_trie import Trie


class Hyphenation:
    """
    Syllabification or syllabication, also known as hyphenation, is the separation of a word into syllables, whether spoken, written or signed.
    A hyphenation algorithm is a set of rules, especially one codified for implementation in a computer program,
    that decides at which points a word can be broken over two lines with a hyphen.
    For example, a hyphenation algorithm might decide that impeachment can be broken as impeach-ment or im-peachment but not impe-achment.
    One of the reasons for the complexity of the rules of word-breaking is that different "dialects" of English tend to differ on hyphenation[citation needed]:
    American English tends to work on sound,
    but British English tends to look to the origins of the word and then to sound.
    There are also a large number of exceptions, which further complicates matters.
    """

    def __init__(self, iso_language_code: str):
        self._patterns: Trie = Trie()
        self._min_prefix_length: int = 128
        self._max_prefix_length: int = 0
        self._min_suffix_length: int = 128
        self._max_suffix_length: int = 0
        self._exceptions: typing.List[str] = []

        # load data
        resources_dir: Path = Path(__file__).parent / "resources"
        hyphenation_pattern_file: Path = resources_dir / ("%s.json" % iso_language_code)
        assert hyphenation_pattern_file.exists(), (
            "No hyphenation file for %s" % iso_language_code
        )
        with open(hyphenation_pattern_file, "r") as json_file_handle:
            data = json.loads(json_file_handle.read())

            # load patterns
            for p in data["patterns"]:
                assert isinstance(p, str)
                for i in range(0, len(p)):
                    if not p[i].isdigit():
                        continue
                    prefix: str = "".join([c for c in p[0:i] if not c.isdigit()])
                    suffix: str = "".join([c for c in p[i:] if not c.isdigit()])
                    # keep track of prefix length
                    self._max_prefix_length = max(self._max_prefix_length, len(prefix))
                    self._min_prefix_length = min(self._min_prefix_length, len(prefix))
                    # keep track of suffix length
                    self._max_suffix_length = max(self._max_suffix_length, len(suffix))
                    self._min_suffix_length = min(self._min_suffix_length, len(suffix))
                    # insert into trie
                    digit: int = int(p[i])
                    self._patterns[prefix + "0" + suffix] = digit

            # load exceptions
            if "exceptions" in data:
                for e in data["exceptions"]:
                    self._exceptions.append(e)

    def hyphenate(self, s: str, hyphenation_character: str = chr(173)) -> str:
        """
        This function hyphenates the input word, inserting the hyphenation_character wherever the word *can* be split
        in syllables. This function returns the word with hyphenation_character inserted.
        """
        # don't spend effort on stupid input
        assert len(hyphenation_character) == 1
        if len(s) <= 1:
            return s

        # check exceptions
        for e in self._exceptions:
            e_raw_str: str = "".join([c for c in e if c.isalpha()])
            if e_raw_str == s:
                return "".join([c if c.isalpha() else hyphenation_character for c in e])

        # normal run of the algorithm
        s2: str = "." + s + "."
        hyphenation_info: typing.List[int] = [0 for _ in range(0, len(s2))]
        for i in range(2, len(s2)):
            for j in range(self._min_prefix_length, self._max_prefix_length + 1):
                if i - j < 0:
                    continue
                prefix: str = s2[(i - j) : i]
                for k in range(self._min_suffix_length, self._max_suffix_length + 1):
                    if j == 0 and k == 0:
                        continue
                    if i + k > len(s):
                        continue
                    suffix: str = s2[i : (i + k)]
                    value: typing.Optional[int] = self._patterns[prefix + "0" + suffix]
                    if value:
                        hyphenation_info[i] = max(hyphenation_info[i], value)
        s3: str = ""
        for i in range(1, len(hyphenation_info) - 1):
            if hyphenation_info[i] % 2 == 1:
                s3 += hyphenation_character + s2[i]
            else:
                s3 += s2[i]
        return s3
