#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts all text from a PDF Document,
    substituting composite glyphs for their simpler representations
"""
import io
import typing

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


class SimpleNonLigatureTextExtraction(SimpleTextExtraction):
    """
    This implementation of EventListener extracts all text from a PDF Document,
    substituting composite glyphs for their simpler representations
    """

    #
    # CONSTRUCTOR
    #

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

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_text(self) -> typing.Dict[int, str]:
        """
        This function returns all text on a given PDF
        """
        out: typing.Dict[int, str] = {}
        for k0, v0 in self._text_per_page.items():
            text = self._text_per_page[k0]
            while any([k1 in text for k1, v1 in self._ligatures_to_replace.items()]):
                for k3, v3 in self._ligatures_to_replace.items():
                    text = text.replace(k3, v3)
            out[k0] = text
        return out

    @staticmethod
    def get_text_from_pdf(pdf: Document) -> typing.Dict[int, str]:
        """
        This function returns the text for a given PDF (per page)
        :param pdf:     the PDF to be analyzed
        :return:        the text per page (represented by typing.Dict[int, str])
        """
        text_per_page: typing.Dict[int, str] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])
            # register EventListener
            l: "SimpleNonLigatureTextExtraction" = SimpleNonLigatureTextExtraction()
            # process Page
            l._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [l])
            l._event_occurred(EndPageEvent(page))
            # add to output dictionary
            text_per_page[page_nr] = l.get_text()[0]
        # return
        return text_per_page
