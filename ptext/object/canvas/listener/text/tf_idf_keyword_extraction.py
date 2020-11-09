import re
from math import log
from typing import List, Optional

from ptext.object.canvas.listener.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from ptext.object.page.page import Page


class TFIDFKeyword:
    def __init__(
        self,
        text: str,
        page_number: int,
        term_frequency: int,
        number_of_pages: int,
        words_on_page: int,
    ):
        self.text = text
        self.page_number = page_number
        self.words_on_page = words_on_page
        self.term_frequency = term_frequency
        self.occurs_on_pages = [self.page_number]
        self.number_of_pages = number_of_pages

    def get_tf_idf_score(self):
        tf = self.term_frequency / self.words_on_page
        idf = log(self.number_of_pages / (1 + len(self.occurs_on_pages)))
        return (tf + 0.001) * (idf + 0.001)

    def __str__(self):
        return "TFIDFKeyword(number_of_pages=%d, occurs_on_pages=%s, term_frequency=%d, text='%s', words_on_page=%d, tf_idf=%10.10f)" % (
            self.number_of_pages,
            str(self.occurs_on_pages),
            self.term_frequency,
            self.text,
            self.words_on_page,
            self.get_tf_idf_score(),
        )


class TFIDFKeywordExtraction(SimpleTextExtraction):
    def __init__(self, stopwords: List[str] = [], minimum_term_frequency: int = 3):
        super().__init__()
        self.keywords = []
        self.stopwords = [x.upper() for x in stopwords]
        self.number_of_pages = 0
        self.minimum_term_frequency = minimum_term_frequency

    def end_page(self, page: Page):
        super().end_page(page)

        # update number of pages
        self.number_of_pages += 1

        # get words
        words = [
            x.upper()
            for x in re.split("[^a-zA-Z]+", self.get_text(self.current_page))
            if x.upper() not in self.stopwords
        ]

        # update dictionary
        for w in words:
            kw = [
                x
                for x in self.keywords
                if x.page_number == self.current_page and x.text == w
            ]
            if len(kw) == 0:
                self.keywords.append(
                    TFIDFKeyword(
                        text=w,
                        page_number=self.current_page,
                        term_frequency=0,
                        number_of_pages=self.number_of_pages,
                        words_on_page=len(words),
                    )
                )
            for kw in [x for x in self.keywords if x.text == w]:
                if kw.page_number == self.current_page:
                    kw.term_frequency += 1
                if self.current_page not in kw.occurs_on_pages:
                    kw.occurs_on_pages.append(self.current_page)

        # update number of pages
        for k in self.keywords:
            k.number_of_pages = self.number_of_pages

    def get_keywords(
        self, page_number: int, limit: Optional[int] = None
    ) -> List[TFIDFKeyword]:
        out = sorted(
            [
                x
                for x in self.keywords
                if x.page_number == page_number
                and (x.term_frequency > self.minimum_term_frequency)
            ],
            key=TFIDFKeyword.get_tf_idf_score,
        )
        if limit is not None:
            out = out[-limit:]
        return out
