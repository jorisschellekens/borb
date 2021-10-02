#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    In information retrieval, tf–idf, TF*IDF, or TFIDF, short for term frequency–inverse document frequency,
    is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.
    It is often used as a weighting factor in searches of information retrieval, text mining, and user modeling.

    The tf–idf value increases proportionally to the number of times a word appears in the document
    and is offset by the number of documents in the corpus that contain the word,
    which helps to adjust for the fact that some words appear more frequently in general.

    tf–idf is one of the most popular term-weighting schemes today.
    A survey conducted in 2015 showed that 83% of text-based recommender systems in digital libraries use tf–idf.

    Variations of the tf–idf weighting scheme are often used by search engines as a central tool
    in scoring and ranking a document's relevance given a user query.
    tf–idf can be successfully used for stop-words filtering in various subject fields,
    including text summarization and classification.

    One of the simplest ranking functions is computed by summing the tf–idf for each query term;
    many more sophisticated ranking functions are variants of this simple model.
"""
import re
import typing
from math import log

from borb.pdf.page.page import Page
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


class TFIDFKeywordExtraction(SimpleTextExtraction):
    """
    In information retrieval, tf–idf, TF*IDF, or TFIDF, short for term frequency–inverse document frequency,
    is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.
    It is often used as a weighting factor in searches of information retrieval, text mining, and user modeling.

    The tf–idf value increases proportionally to the number of times a word appears in the document
    and is offset by the number of documents in the corpus that contain the word,
    which helps to adjust for the fact that some words appear more frequently in general.

    tf–idf is one of the most popular term-weighting schemes today.
    A survey conducted in 2015 showed that 83% of text-based recommender systems in digital libraries use tf–idf.

    Variations of the tf–idf weighting scheme are often used by search engines as a central tool
    in scoring and ranking a document's relevance given a user query.
    tf–idf can be successfully used for stop-words filtering in various subject fields,
    including text summarization and classification.

    One of the simplest ranking functions is computed by summing the tf–idf for each query term;
    many more sophisticated ranking functions are variants of this simple model.
    """

    def __init__(
        self, stopwords: typing.List[str] = [], minimum_term_frequency: int = 3
    ):
        super().__init__()
        self._term_frequency_per_page: typing.Dict[int, typing.Dict[str, float]] = {}
        self._number_of_words_per_page: typing.Dict[int, float] = {}
        self._inverse_page_frequency: typing.Dict[str, float] = {}
        self._stopwords: typing.List[str] = [x.upper() for x in stopwords]
        self._number_of_pages: float = 0
        self._minimum_term_frequency: float = minimum_term_frequency

    def _end_page(self, page: Page):
        super()._end_page(page)

        # update number of pages
        self._number_of_pages += 1

        # get words
        words_on_page: typing.List[str] = [
            x.upper()
            for x in re.split("[^a-zA-Z]+", self.get_text_for_page(self._current_page))
            if x.upper() not in self._stopwords
        ]

        # update _term_frequency_per_page
        self._term_frequency_per_page[self._current_page] = {}
        self._number_of_words_per_page[self._current_page] = len(words_on_page)
        for w in words_on_page:
            self._term_frequency_per_page[self._current_page][w] = (
                self._term_frequency_per_page[self._current_page].get(w, 0) + 1
            )

        # update _inverse_page_frequency
        for w in set(words_on_page):
            self._inverse_page_frequency[w] = self._inverse_page_frequency.get(w, 0) + 1

    def get_keywords_for_page(
        self, page_number: int
    ) -> typing.List[typing.Tuple[str, float]]:
        """
        This function returns a typing.List[typing.Tuple[str, float]] for a given page
        """
        out: typing.List[typing.Tuple[str, float]] = []
        for w, tf in self._term_frequency_per_page[page_number].items():

            # check minimum_term_frequency
            if tf < self._minimum_term_frequency:
                continue

            # normalize tf, idf
            tf /= self._number_of_words_per_page[page_number]
            idf = log(self._number_of_pages / self._inverse_page_frequency[w])

            # avoid multiply by zero
            tf += 0.0001
            idf += 0.0001

            # calculate tf-idf score
            out.append((w, tf * idf))

        # sort
        out.sort(key=lambda x: x[1], reverse=True)

        # return
        return out
