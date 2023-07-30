#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TextRank – is a graph-based ranking model for text processing which can be used in order to find the most relevant sentences in text and also to find keywords.
The algorithm is explained in detail in the paper at https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf

In order to find relevant keywords, the textrank algorithm constructs a word network.
This network is constructed by looking which words follow one another.
A link is set up between two words if they follow one another, the link gets a higher weight if these 2 words occur more frequenctly next to each other in the text.

On top of the resulting network the Pagerank algorithm is applied to get the importance of each word.
The top 1/3 of all these words are kept and are considered relevant.
After this, a keywords table is constructed by combining the relevant words together if they appear following one another in the text.
"""
import io
import re
import typing

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction
from borb.toolkit.text.stop_words import ENGLISH_STOP_WORDS


class TextRankKeywordExtraction(SimpleTextExtraction):
    """
    TextRank – is a graph-based ranking model for text processing which can be used in order to find the most relevant sentences in text and also to find keywords.
    The algorithm is explained in detail in the paper at https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf

    In order to find relevant keywords, the textrank algorithm constructs a word network.
    This network is constructed by looking which words follow one another.
    A link is set up between two words if they follow one another, the link gets a higher weight if these 2 words occur more frequenctly next to each other in the text.

    On top of the resulting network the Pagerank algorithm is applied to get the importance of each word.
    The top 1/3 of all these words are kept and are considered relevant.
    After this, a keywords table is constructed by combining the relevant words together if they appear following one another in the text.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__()
        self._stopwords = [x.upper() for x in ENGLISH_STOP_WORDS]

        # keep track of keywords_per_page
        self._keywords_per_page: typing.Dict[
            int, typing.List[typing.Tuple[str, float]]
        ] = {}

    #
    # PRIVATE
    #

    def _end_page(self, page: Page):
        super()._end_page(page)

        # extract text
        txt: str = super(TextRankKeywordExtraction, self).get_text()[self._current_page]

        # transfer matrix
        mtx: typing.Dict[str, typing.Dict[str, float]] = {}

        # turn txt into lines
        lines = [x for x in re.split("\n*[.?!]+\n*", txt) if len(x) != 0]
        for line in lines:
            # split
            tokens: typing.List[str] = [
                x for x in re.split("[^A-Z]+", line.upper()) if len(x) > 3
            ]

            # build transfer matrix
            for i0 in range(0, len(tokens)):
                w0: str = tokens[i0].upper()
                if w0 not in mtx:
                    mtx[w0] = {}
                for i1 in range(-3, 3):
                    if i0 + i1 < 0 or i0 + i1 >= len(tokens) or i1 == 0:
                        continue
                    w1: str = tokens[i0 + i1].upper()
                    mtx[w0][w1] = mtx[w0].get(w1, 0) + 1

        # run eigenvalue algorithm
        ws: typing.List[str] = [x for x, _ in mtx.items()]
        eigenvalues_001: typing.Dict[str, float] = {x: 1 for x in ws}
        eigenvalues_002: typing.Dict[str, float] = {x: 0 for x in ws}
        delta: float = 1
        number_of_iterations: int = 0
        while delta > 0.0001 and number_of_iterations < 128:
            for w0 in ws:
                n: int = len(mtx[w0])
                for w1, f1 in mtx[w0].items():
                    eigenvalues_002[w1] += f1 * (eigenvalues_001[w0] / n)

            # calculate delta
            delta = max([abs(eigenvalues_001[x] - eigenvalues_002[x]) for x in ws])
            number_of_iterations += 1

            # update eigenvalues
            total_weight: float = sum([f for _, f in eigenvalues_002.items()])
            eigenvalues_001 = {
                x: (f / total_weight) for x, f in eigenvalues_002.items()
            }
            eigenvalues_002 = {x: 0 for x, _ in mtx.items()}

        # store keywords
        # fmt: off
        self._keywords_per_page[self._current_page] = [(x, f) for x, f in eigenvalues_001.items()]
        self._keywords_per_page[self._current_page].sort(key=lambda x: x[1], reverse=True)
        # fmt: on

    #
    # PUBLIC
    #

    def get_keywords(self) -> typing.Dict[int, typing.List[typing.Tuple[str, float]]]:
        """
        This function returns a typing.List[TextRankKeyword] for a given PDF
        """
        return self._keywords_per_page

    @staticmethod
    def get_keywords_from_pdf(
        pdf: Document,
    ) -> typing.Dict[int, typing.List[typing.Tuple[str, float]]]:
        """
        This function returns the keywords for a given PDF (per page)
        :param pdf:     the PDF to be analyzed
        :return:        the keywords per page (represented by typing.Dict[int, typing.List[typing.Tuple[str, float]]])
        """
        keywords_per_page: typing.Dict[int, typing.List[typing.Tuple[str, float]]] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])
            # register EventListener
            l: "TextRankKeywordExtraction" = TextRankKeywordExtraction()
            # process Page
            l._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [l])
            l._event_occurred(EndPageEvent(page))
            # add to output dictionary
            keywords_per_page[page_nr] = l.get_keywords()[0]
        # return
        return keywords_per_page
