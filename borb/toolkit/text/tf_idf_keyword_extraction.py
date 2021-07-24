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
from typing import List, Optional

from borb.pdf.page.page import Page
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


class TFIDFKeyword:
    """
    This class represents a TF-IDF keyword and its associated meta-data
    """

    def __init__(
        self,
        text: str,
        page_number: int,
        term_frequency: int,
        number_of_pages: int,
        words_on_page: int,
    ):
        self._text: str = text
        self._page_number: int = page_number
        self._words_on_page: int = words_on_page
        self._term_frequency: int = term_frequency
        self._occurs_on_pages = [self._page_number]
        self._number_of_pages: int = number_of_pages

    def get_text(self) -> str:
        """
        This function returns the text of this TFIDFKeyword
        """
        return self._text

    def get_term_frequency(self) -> int:
        """
        This function returns the term frequency of this TFIDFKeyword
        """
        return self._term_frequency

    def get_page_number(self) -> int:
        """
        This function returns the page number of this TFIDFKeyword
        """
        return self._page_number

    def get_number_of_words_on_page(self) -> int:
        """
        This function returns the number of words on the page
        associated with this TFIDFKeyword
        """
        return self._words_on_page

    def get_number_of_pages(self) -> int:
        """
        This function returns the number of pages in the
        document associated with this TFIDFKeyword
        """
        return self._number_of_pages

    def get_tf_idf_score(self) -> float:
        """
        This function returns the TF-IDF score for this keyword
        """
        tf = self._term_frequency / self._words_on_page
        idf = log(self._number_of_pages / (1 + len(self._occurs_on_pages)))
        return (tf + 0.001) * (idf + 0.001)


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
        self._keywords: typing.List[TFIDFKeyword] = []
        self._stopwords = [x.upper() for x in stopwords]
        self._number_of_pages = 0
        self._minimum_term_frequency = minimum_term_frequency

    def _end_page(self, page: Page):
        super()._end_page(page)

        # update number of pages
        self._number_of_pages += 1

        # get words
        words = [
            x.upper()
            for x in re.split("[^a-zA-Z]+", self.get_text(self._current_page))
            if x.upper() not in self._stopwords
        ]

        # update dictionary
        for w in words:
            keywords_on_same_page = [
                x
                for x in self._keywords
                if x._page_number == self._current_page and x._text == w
            ]
            if len(keywords_on_same_page) == 0:
                self._keywords.append(
                    TFIDFKeyword(
                        text=w,
                        page_number=self._current_page,
                        term_frequency=0,
                        number_of_pages=self._number_of_pages,
                        words_on_page=len(words),
                    )
                )
            for keyword in [x for x in self._keywords if x._text == w]:
                assert isinstance(keyword, TFIDFKeyword)
                if keyword._page_number == self._current_page:
                    keyword._term_frequency += 1
                if self._current_page not in keyword._occurs_on_pages:
                    keyword._occurs_on_pages.append(self._current_page)

        # update number of pages
        for k in self._keywords:
            k._number_of_pages = self._number_of_pages

    def get_keywords_per_page(
        self, page_number: int, limit: Optional[int] = None
    ) -> List[TFIDFKeyword]:
        """
        This function returns a typing.List[TFIDFKeyword] for a given page
        """
        out = sorted(
            [
                x
                for x in self._keywords
                if x._page_number == page_number
                and (x._term_frequency > self._minimum_term_frequency)
            ],
            key=TFIDFKeyword.get_tf_idf_score,
        )
        if limit is not None:
            out = out[-limit:]
        return out
