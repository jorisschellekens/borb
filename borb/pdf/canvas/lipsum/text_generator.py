#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a simple Markov model to generate text.
"""
import json
import random
import re
import typing
import zlib
import pathlib
import requests


class TextGenerator:
    """
    This class represents a simple Markov model to generate text.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._markov_model: typing.Dict[
            typing.Tuple[int, int], typing.Dict[int, int]
        ] = {}
        self._rev_token_ids: typing.Dict[int, str] = {}
        self._token_frequency: typing.Dict[int, int] = {}
        self._token_ids: typing.Dict[str, int] = {}

    #
    # PRIVATE
    #

    def __len__(self):
        return len(self._token_ids)

    @staticmethod
    def _is_valid_token(s: str) -> bool:
        # forbid tokens of length 0
        if len(s) == 0:
            return False
        # forbid tokens that contain non-alphanumeric characters
        if any([not (x.isalnum() or x in ".?!,") for x in s]):
            return False
        # forbid tokens that consist solely of uppercase
        if s.upper() == s:
            return False
        # forbid tokens that consist solely of numbers
        if s.isnumeric():
            return False
        return True

    def _train_using_project_gutenberg(self, gutenberg_url: str) -> "TextGenerator":
        training_text: str = requests.get(gutenberg_url).text

        # trim header:
        header_text: str = "*** START OF THE PROJECT GUTENBERG EBOOK"
        if header_text in training_text:
            start_pos: int = training_text.find(
                "***", training_text.find(header_text) + len(header_text)
            ) + len("***")
            training_text = training_text[start_pos:]
        # trim footer
        footer_text: str = "*** END OF THE PROJECT GUTENBERG EBOOK"
        if footer_text in training_text:
            end_pos: int = training_text.find(footer_text)
            training_text = training_text[0:end_pos]
        # tokenize, build model
        tokens: typing.List[str] = re.split("[ \n\t\r]+", training_text)
        self._token_ids = {}
        self._rev_token_ids = {}
        self._token_frequency = {}
        self._markov_model = {}
        for i in range(0, len(tokens) - 2):
            # get token, set/create ID
            t0: str = tokens[i].strip(" \n\t")
            if not TextGenerator._is_valid_token(t0):
                continue
            t0_id: int = self._token_ids.get(t0, len(self._token_ids))
            self._token_ids[t0] = t0_id

            # get token, set/create ID
            t1: str = tokens[i + 1].strip(" \n\t")
            if not TextGenerator._is_valid_token(t1):
                continue
            t1_id: int = self._token_ids.get(t1, len(self._token_ids))
            self._token_ids[t1] = t1_id

            # get token, set/create ID
            t2: str = tokens[i + 2].strip(" \n\t")
            if not TextGenerator._is_valid_token(t2):
                continue
            t2_id: int = self._token_ids.get(t2, len(self._token_ids))
            self._token_ids[t2] = t2_id

            # update frequency
            self._token_frequency[t0_id] = self._token_frequency.get(t0_id, 0) + 1

            # update markov model
            mm_key: typing.Tuple[int, int] = (t0_id, t1_id)
            if mm_key not in self._markov_model:
                self._markov_model[mm_key] = {}
            self._markov_model[mm_key][t2_id] = (
                self._markov_model[mm_key].get(t2_id, 0) + 1
            )
        # reverse ID map
        self._rev_token_ids = {v: k for k, v in self._token_ids.items()}

        # return
        return self

    #
    # PUBLIC
    #

    def generate(self, min_sentence_length: int = 32) -> str:
        """
        This function generates a string using the statistical model
        stored in this TextGenerator
        :param min_sentence_length:     the minimal sentence length (in tokens)
        :return:                        a string
        """
        # build some text
        sentence_being_built: typing.List[str] = []

        # build text
        while len(
            sentence_being_built
        ) < min_sentence_length or not sentence_being_built[-1].endswith("."):
            # init
            if len(sentence_being_built) == 0:
                seed: typing.Tuple[int, int] = random.choice(
                    [
                        (t0, t1)
                        for (t0, t1) in self._markov_model.keys()
                        if len(self._rev_token_ids[t0]) > 0
                        and self._rev_token_ids[t0][0]
                        == self._rev_token_ids[t0][0].upper()
                    ]
                )
                sentence_being_built.append(self._rev_token_ids[seed[0]])
                sentence_being_built.append(self._rev_token_ids[seed[1]])
                continue

            # default
            t0_id: int = self._token_ids[sentence_being_built[-2]]
            t1_id: int = self._token_ids[sentence_being_built[-1]]

            # build key
            mm_key: typing.Tuple[int, int] = (t0_id, t1_id)
            if mm_key not in self._markov_model:
                sentence_being_built = []
                continue

            # select next element
            nexts: typing.Dict[int, int] = self._markov_model[mm_key]
            ops: typing.List[int] = []
            for k, v in nexts.items():
                for _ in range(0, v):
                    ops.append(k)
            if len(sentence_being_built) < min_sentence_length:
                sentence_being_built.append(self._rev_token_ids[random.choice(ops)])
            else:
                end_sentence_ops: typing.List[int] = [
                    x for x in ops if self._rev_token_ids[x].endswith(".")
                ]
                if len(end_sentence_ops) == 0:
                    sentence_being_built.append(self._rev_token_ids[random.choice(ops)])
                else:
                    sentence_being_built.append(
                        self._rev_token_ids[random.choice(end_sentence_ops)]
                    )

        # return
        return "".join([x + " " for x in sentence_being_built])

    def load(self, json_file: pathlib.Path) -> "TextGenerator":
        """
        This function loads a TextGenerator from a (zipped) JSON file
        :param json_file:   the location where to load the (zipped) JSON
        :return:            self
        """
        with open(json_file, "rb") as json_file_handle:
            json_obj = json.loads(zlib.decompress(json_file_handle.read()))
        (
            self._token_ids,
            self._rev_token_ids,
            self._token_frequency,
            self._markov_model,
        ) = (
            {k: int(v) for k, v in json_obj["token_ids"].items()},
            {int(k): v for k, v in json_obj["rev_token_ids"].items()},
            {int(k): int(v) for k, v in json_obj["token_frequency"].items()},
            {
                (int(k.split("|")[0]), int(k.split("|")[1])): {
                    int(a): int(b) for a, b in v.items()
                }
                for k, v in json_obj["markov_model"].items()
            },
        )
        return self

    def store(self, file_name: str) -> None:
        """
        This function stores this TextGenerator in a (zipped) JSON format
        :param file_name:   the location where to store the (zipped) JSON
        :return:            None
        """
        with open(file_name, "wb") as json_file_handle:
            json_file_handle.write(
                zlib.compress(
                    bytes(
                        json.dumps(
                            {
                                "token_ids": self._token_ids,
                                "rev_token_ids": self._rev_token_ids,
                                "token_frequency": self._token_frequency,
                                "markov_model": {
                                    str(k[0]) + "|" + str(k[1]): v
                                    for k, v in self._markov_model.items()
                                },
                            }
                        ),
                        encoding="utf8",
                    ),
                    level=9,
                )
            )
