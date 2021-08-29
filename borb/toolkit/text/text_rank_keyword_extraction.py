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
import json
import re
import typing
from pathlib import Path

from borb.pdf.page.page import Page
from borb.toolkit.text.bigram_part_of_speech_tagger import BigramPartOfSpeechTagger
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

    def __init__(self):
        super().__init__()
        self._stopwords = [x.upper() for x in ENGLISH_STOP_WORDS]

        # set up part of speech tagger
        self._part_of_speech_tagger: BigramPartOfSpeechTagger = (
            BigramPartOfSpeechTagger()
        )
        bigram_tagger_file: Path = (
            Path(__file__).parent / "bigram_part_of_speech_tagger_en.json"
        )
        with open(bigram_tagger_file, "r") as json_file_handle:
            self._part_of_speech_tagger.from_json(json.loads(json_file_handle.read()))

        # keep track of keywords_per_page
        self._keywords_per_page: typing.Dict[
            int, typing.List[typing.Tuple[str, float]]
        ] = {}

    def _end_page(self, page: Page):
        super()._end_page(page)

        # extract text
        txt: str = super(TextRankKeywordExtraction, self).get_text_for_page(
            self._current_page
        )

        # transfer matrix
        mtx: typing.Dict[str, typing.Dict[str, float]] = {}

        # turn txt into lines
        lines = [x for x in re.split("\n*[.?!]+\n*", txt) if len(x) != 0]
        for line in lines:

            # POS tagging
            tags_and_tokens: typing.List[
                typing.Tuple[str, str]
            ] = self._part_of_speech_tagger.tag_str(line)

            # select only NOUN, ADJ
            toks = [x[0] for x in tags_and_tokens if x[1] in ["nn", "jj"]]

            # build transfer matrix
            for i0 in range(0, len(toks)):
                w0: str = toks[i0].upper()
                if w0 not in mtx:
                    mtx[w0] = {}
                for i1 in range(-3, 3):
                    if i0 + i1 < 0 or i0 + i1 >= len(toks) or i1 == 0:
                        continue
                    w1: str = toks[i0 + i1].upper()
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
        self._keywords_per_page[self._current_page] = [
            (x, f) for x, f in eigenvalues_001.items()
        ]
        self._keywords_per_page[self._current_page].sort(
            key=lambda x: x[1], reverse=True
        )

    def get_keywords_for_page(self, page_number: int) -> typing.List[typing.Any]:
        """
        This function returns a typing.List[TextRankKeyword] for a given page
        """
        return self._keywords_per_page.get(page_number, [])
