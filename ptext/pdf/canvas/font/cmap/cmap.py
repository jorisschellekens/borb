#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A CMap shall specify the mapping from character codes to character selectors. In PDF, the character selectors
    shall be CIDs in a CIDFont (as mentioned earlier, PostScript CMaps can use names or codes as well). A CMap
    serves a function analogous to the Encoding dictionary for a simple font. The CMap shall not refer directly to a
    specific CIDFont; instead, it shall be combined with it as part of a CID-keyed font, represented in PDF as a
    Type 0 font dictionary (see 9.7.6, "Type 0 Font Dictionaries"). Within the CMap, the character mappings shall
    refer to the associated CIDFont by font number, which in PDF shall be 0.
"""
import io
from typing import Union, List, Optional, Tuple

from ptext.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.io.read.tokenize.low_level_tokenizer import Token
from ptext.io.read.types import HexadecimalString


class CMap:
    """
    A CMap shall specify the mapping from character codes to character selectors. In PDF, the character selectors
    shall be CIDs in a CIDFont (as mentioned earlier, PostScript CMaps can use names or codes as well). A CMap
    serves a function analogous to the Encoding dictionary for a simple font. The CMap shall not refer directly to a
    specific CIDFont; instead, it shall be combined with it as part of a CID-keyed font, represented in PDF as a
    Type 0 font dictionary (see 9.7.6, "Type 0 Font Dictionaries"). Within the CMap, the character mappings shall
    refer to the associated CIDFont by font number, which in PDF shall be 0.
    """

    def __init__(self):
        self._unicode_to_code = {}
        self._code_to_unicode = {}

    def unicode_to_code(self, unicode: Union[int, List[int]]) -> Optional[int]:
        """
        Converts a unicode code point to a character code
        Returns None if this CMAP does not contain a mapping for the given unicode code point
        """
        return self._unicode_to_code.get(unicode)

    def code_to_unicode(self, character_code: int) -> Optional[int]:
        """
        Converts a character code to a unicode code point
        Returns None if this CMAP does not contain a mapping for the given character code
        """
        return self._code_to_unicode.get(character_code, None)

    def _add_symbol(
        self, character_code: int, unicode: Union[int, Tuple[int, ...]]
    ) -> "CMap":
        self._unicode_to_code[unicode] = character_code
        self._code_to_unicode[character_code] = unicode
        return self

    def can_encode_unicode(self, unicode: Union[int, List[int]]) -> bool:
        """
        Return True if this CMAP can encode the given unicode code point, False otherwise
        """
        return unicode in self._unicode_to_code

    def can_encode_character_code(self, character_code: int) -> bool:
        """
        Return True if this CMAP can encode the given character code, False otherwise
        """
        return character_code in self._code_to_unicode

    def read(self, cmap_bytes: str) -> "CMap":

        N = len(cmap_bytes)
        tok = HighLevelTokenizer(io.BytesIO(cmap_bytes.encode("latin-1")))

        prev_token: Optional[Token] = None
        while tok.tell() < N:

            token = tok.next_non_comment_token()
            if token is None:
                break

            # beginbfchar
            if token.text == "beginbfchar":
                assert prev_token is not None
                n = int(prev_token.text)
                for j in range(0, n):
                    obj = tok.read_object()
                    assert isinstance(obj, HexadecimalString)
                    c = self._hex_string_to_int_or_tuple(obj)
                    assert isinstance(c, int)

                    obj = tok.read_object()
                    assert isinstance(obj, HexadecimalString)
                    uc = self._hex_string_to_int_or_tuple(obj)

                    self._add_symbol(c, uc)
                continue

            # beginbfrange
            if token.text == "beginbfrange":
                assert prev_token is not None
                n = int(prev_token.text)
                for j in range(0, n):

                    c_start_token = tok.read_object()
                    assert c_start_token is not None
                    assert isinstance(c_start_token, HexadecimalString)
                    c_start = int(c_start_token, 16)

                    c_end_token = tok.read_object()
                    assert c_end_token is not None
                    assert isinstance(c_end_token, HexadecimalString)
                    c_end = int(c_end_token, 16)

                    tmp = tok.read_object()
                    if isinstance(tmp, HexadecimalString):
                        uc = self._hex_string_to_int_or_tuple(tmp)
                        for k in range(0, c_end - c_start + 1):
                            if isinstance(uc, int):
                                self._add_symbol(c_start + k, uc + k)
                            elif isinstance(uc, tuple):
                                self._add_symbol(c_start + k, (uc[0], uc[1] + k))

                    elif isinstance(tmp, list):
                        for k in range(0, c_end - c_start + 1):
                            uc = self._hex_string_to_int_or_tuple(tmp[k])
                            self._add_symbol(c_start + k, uc)

            # default
            prev_token = token

        return self

    def _hex_string_to_int_or_tuple(
        self, token: HexadecimalString
    ) -> Union[int, Tuple[int, ...]]:
        uc_hex = token.replace(" ", "")
        uc = [int(uc_hex[k : k + 4], 16) for k in range(0, int(len(uc_hex)), 4)]
        return tuple(uc) if len(uc) > 1 else uc[0]
