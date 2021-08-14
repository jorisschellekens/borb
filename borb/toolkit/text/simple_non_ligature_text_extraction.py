#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts all text from a PDF Document,
    substituting composite glyphs for their simpler representations
"""
import typing

from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


class SimpleNonLigatureTextExtraction(SimpleTextExtraction):
    """
    This implementation of EventListener extracts all text from a PDF Document,
    substituting composite glyphs for their simpler representations
    """

    def __init__(self):
        super(SimpleNonLigatureTextExtraction, self).__init__()
        self._ligatures_to_replace: typing.Dict[str, str] = {
            "Ꜳ": "AA",
            "ꜳ": "aa",
            "Æ": "AE",
            "æ": "ae",
            "ꬱ": "aə",
            "Ꜵ": "AO",
            "ꜵ": "ao",
            "Ꜷ": "AU",
            "ꜷ": "au",
            "Ꜹ": "AV",
            "ꜹ": "av",
            "Ꜻ": "AV",
            "ꜻ": "av",
            "Ꜽ": "AY",
            "ꜽ": "ay",
            "🙰": "et",
            "ꭁ": "əø",
            "ﬀ": "ff",
            "ﬃ": "ffi",
            "ﬄ": "ffl",
            "ﬁ": "fi",
            "ﬂ": "fl",
            "℔": "lb",
            "Ỻ": "IL",
            "ỻ": "ll",
            "Œ": "OE",
            "œ": "oe",
            "Ꝏ": "OO",
            "ꝏ": "oo",
            "ꭢ": "ɔe",
            "ſs": "ẞ",
            "ſz": "ß",
            "ﬆ": "st",
            "ﬅ": "ſt",
            "Ꜩ": "TZ",
            "ꜩ": "tz",
            "ᵫ": "ue",
            "ꭣ": "uo",
            "W": "VV",
            "w": "vv",
            "Ꝡ": "VY",
            "ꝡ": "vy",
        }

    def get_text_for_page(self, page_nr: int) -> str:
        """
        This function returns all text on a given page
        """
        text: str = ""
        if page_nr in self._text_per_page:
            text = self._text_per_page[page_nr]
            while any([k in text for k, v in self._ligatures_to_replace]):
                for k, v in self._ligatures_to_replace.items():
                    text = text.replace(k, v)
        return text
