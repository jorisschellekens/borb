#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class is the simplest implementation of a Part-of-Speech (POS) tagger
that still works reliably enough for keyword extraction.
In corpus linguistics, part-of-speech tagging (POS tagging or PoS tagging or POST),
also called grammatical tagging is the process of marking up a word in a text (corpus) as corresponding to a particular part of speech,
based on both its definition and its context. A simplified form of this is commonly taught to school-age children,
in the identification of words as nouns, verbs, adjectives, adverbs, etc.
"""
import json
import re
import typing
from decimal import Decimal
from pathlib import Path


class BigramPartOfSpeechTagger:
    """
    This class is the simplest implementation of a Part-of-Speech (POS) tagger
    that still works reliably enough for keyword extraction.
    In corpus linguistics, part-of-speech tagging (POS tagging or PoS tagging or POST),
    also called grammatical tagging is the process of marking up a word in a text (corpus) as corresponding to a particular part of speech,
    based on both its definition and its context. A simplified form of this is commonly taught to school-age children,
    in the identification of words as nouns, verbs, adjectives, adverbs, etc.
    """

    def __init__(self):
        self._tags_per_word: typing.Dict[str, typing.Dict[str, int]] = {}
        self._2_step_transitions: typing.Dict[typing.Tuple[str, str], int] = {}
        self._tags_per_word_ending: typing.Dict[str, typing.Dict[str, int]] = {}
        self._odds_best_tagging: typing.Optional[Decimal] = None
        self._best_tagging: typing.List[str] = []

    def _train_on_brown_corpus_dir(
        self, brown_corpus_file: Path
    ) -> "BigramPartOfSpeechTagger":
        """
        This method trains this BigramPartOfSpeechTagger on
        a corpus (in the Brown Corpus format)
        """
        i: int = 0
        for corpus_file in brown_corpus_file.iterdir():
            if i >= 500:
                break
            if len(corpus_file.name) == 4:
                self._train_on_file(corpus_file)
                print("training .. [%d / %d]" % (i + 1, 500))
                i += 1
        return self

    def from_json(self, json_data) -> "BigramPartOfSpeechTagger":
        """
        This function loads a BigramPartOfSpeechTagger from
        its JSON representation.
        This function returns self.
        """
        self._tags_per_word = json_data["_tags_per_word"]
        self._2_step_transitions = {
            (t.split("_")[0], t.split("_")[1]): f
            for t, f in json_data["_2_step_transitions"].items()
        }
        self._tags_per_word_ending = json_data["_tags_per_word_ending"]
        return self

    def to_json(self) -> typing.Dict:
        """
        This function stores this BigramPartOfSpeechTagger as
        its JSON representation.
        This function returns typing.Dict.
        """
        return {
            "_tags_per_word": self._tags_per_word,
            "_2_step_transitions": {
                (t[0] + "_" + t[1]): f for t, f in self._2_step_transitions.items()
            },
            "_tags_per_word_ending": self._tags_per_word_ending,
        }

    def _train_on_file(self, file) -> "BigramPartOfSpeechTagger":
        txt: str = ""
        with open(file, "r") as fh:
            txt = fh.read()
        # split
        lines = re.split("\n+\t*", txt)
        for l in lines:
            self._train_on_line(l)
        # return
        return self

    def _train_on_line(self, line_of_text: str) -> "BigramPartOfSpeechTagger":
        tokens_and_tags: typing.List[typing.Tuple[str, str]] = [
            (x.split("/")[0].upper(), x.split("/")[1])
            for x in line_of_text.split(" ")
            if "/" in x
        ]
        prev_t: typing.Optional[str] = None
        for w, t in tokens_and_tags:
            # update _tags_per_word
            if w not in self._tags_per_word:
                self._tags_per_word[w] = {}
            self._tags_per_word[w][t] = self._tags_per_word[w].get(t, 0) + 1
            # update _tags_per_word_ending
            suffix: str = w[-3:]
            if suffix not in self._tags_per_word_ending:
                self._tags_per_word_ending[suffix] = {}
            self._tags_per_word_ending[suffix][t] = (
                self._tags_per_word_ending[suffix].get(t, 0) + 1
            )
            # update _2_step_transitions
            if prev_t is not None:
                self._2_step_transitions[(prev_t, t)] = (
                    self._2_step_transitions.get((prev_t, t), 0) + 1
                )
            # set everything up for next iteration
            prev_t = t
        # return
        return self

    def _tag_words_that_are_almost_always_the_same(
        self, tokens: typing.List[typing.Optional[str]]
    ) -> typing.List[typing.Optional[str]]:
        tags: typing.List[typing.Optional[str]] = []
        for w in tokens:
            if w is None:
                continue
            w = w.upper()
            if w in self._tags_per_word:
                normalized_tags: typing.Dict[str, float] = {
                    t: f / sum([x for _, x in self._tags_per_word[w].items()])
                    for t, f in self._tags_per_word[w].items()
                }
                max_tag: typing.Optional[str] = None
                for t, f in normalized_tags.items():
                    if max_tag is None or f > normalized_tags[max_tag]:
                        max_tag = t
                assert max_tag is not None
                if normalized_tags[max_tag] > 0.99:
                    tags.append(max_tag)
                else:
                    tags.append(None)
            else:
                tags.append(None)
        return tags

    def _tag_by_transition(
        self,
        tokens: typing.List[str],
        tags: typing.List[typing.Optional[str]],
        tag_odds: typing.List[typing.Optional[Decimal]],
        transition_odds: typing.List[typing.Optional[Decimal]],
    ):

        # determine odds of current configuration
        p: Decimal = Decimal(1)
        for x in tag_odds:
            if x is not None:
                p *= Decimal(x)
        for x in transition_odds:
            if x is not None:
                p *= Decimal(x)
        if self._odds_best_tagging is not None and p < self._odds_best_tagging:
            return

        # determine first_unknown_tag_index
        first_unknown_tag_index: typing.Optional[int] = None
        for i in range(0, len(tokens)):
            if tags[i] is not None:
                continue
            if tags[i] is None:
                first_unknown_tag_index = i
                break

        if first_unknown_tag_index is None:
            if self._odds_best_tagging is None or p > self._odds_best_tagging:
                self._odds_best_tagging = p
                self._best_tagging = [x for x in tags]
            return

        # determine possible tags
        assert first_unknown_tag_index is not None
        w: str = tokens[first_unknown_tag_index].upper()
        possible_tags: typing.Dict[str, Decimal] = {"nn": Decimal(1)}
        if w in self._tags_per_word:
            possible_tags = {
                t: Decimal(f / sum([x for _, x in self._tags_per_word[w].items()]))
                for t, f in self._tags_per_word[w].items()
            }
        if len(possible_tags) == 0:
            suffix: str = w[-3:]
            if suffix in self._tags_per_word_ending:
                possible_tags = {
                    t: Decimal(
                        f
                        / sum(
                            [x for _, x in self._tags_per_word_ending[suffix].items()]
                        )
                    )
                    for t, f in self._tags_per_word_ending[suffix].items()
                }

        # recursion
        prev_tag: typing.Optional[str] = None
        if first_unknown_tag_index != 0:
            prev_tag = tags[first_unknown_tag_index - 1]
        for t, f in possible_tags.items():
            # set tag
            tags[first_unknown_tag_index] = t
            tag_odds[first_unknown_tag_index] = f
            if prev_tag is not None:
                transition_odds[first_unknown_tag_index - 1] = Decimal(
                    self._2_step_transitions.get((prev_tag, t), 0)
                    / sum(
                        [
                            x
                            for p, x in self._2_step_transitions.items()
                            if p[0] == prev_tag
                        ]
                    )
                )

            # recursion
            self._tag_by_transition(tokens, tags, tag_odds, transition_odds)

            # unset tag
            tags[first_unknown_tag_index] = None
            tag_odds[first_unknown_tag_index] = None
            if prev_tag is not None:
                transition_odds[first_unknown_tag_index - 1] = None

    def tag_str(self, s: str) -> typing.List[typing.Tuple[str, str]]:
        """
        This function tags a str.
        It will first perform a rudimentary form of tokenization.
        This function returns typing.List[typing.Tuple[str, str]]
        representing both the original tokens, and their corresponding
        part-of-speech tag.
        """
        toks: typing.List[str] = []
        prev_tok: str = ""
        for c in s:
            if c in ".,?!()[]":
                toks.append(prev_tok)
                toks.append(c)
                prev_tok = ""
                continue
            if c == " ":
                toks.append(prev_tok)
                prev_tok = ""
                continue
            if c == "\n":
                toks.append(prev_tok)
                prev_tok = ""
                continue
            prev_tok += c
        toks.append(prev_tok)
        toks = [x for x in toks if len(x) != 0]
        return [x for x in zip(toks, self.tag_list_str(toks))]

    def tag_list_str(self, tokens: typing.List[str]) -> typing.List[str]:
        """
        This function tags a typing.List[str].
        This function returns typing.List[str] representing the part-of-speech tag of each token.
        """
        if len(tokens) > 16:
            return self.tag_list_str(tokens[0:16]) + self.tag_list_str(tokens[16:])

        # init
        self._odds_best_tagging = None
        self._best_tagging = []

        # easy tagging
        tags: typing.List[
            typing.Optional[str]
        ] = self._tag_words_that_are_almost_always_the_same(tokens)

        # transition_odds
        transition_odds: typing.List[typing.Optional[Decimal]] = []
        for i in range(1, len(tags)):
            if tags[i - 1] is not None and tags[i] is not None:
                p: Decimal = Decimal(
                    self._2_step_transitions.get((tags[i - 1], tags[i]), 0)
                    / sum(
                        [
                            x
                            for j, x in self._2_step_transitions.items()
                            if j[0] == tags[i - 1]
                        ]
                    )
                )
                transition_odds.append(p)
            else:
                transition_odds.append(None)

        # transition tagging
        self._tag_by_transition(
            tokens,
            tags,
            [None if x is None else Decimal(1) for x in tags],
            transition_odds,
        )

        # return
        return self._best_tagging
