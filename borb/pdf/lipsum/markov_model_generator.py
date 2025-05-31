#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class to generate a Markov model used for text generation.

This class constructs a Markov model from a given input corpus, which can
then be used by another class to generate text. The Markov model is built
by analyzing the sequence of words or characters in the input, allowing
for the prediction of the next item in the sequence based on prior data.
"""
import typing


class MarkovModelGenerator:
    """
    A class to generate a Markov model used for text generation.

    This class constructs a Markov model from a given input corpus, which can
    then be used by another class to generate text. The Markov model is built
    by analyzing the sequence of words or characters in the input, allowing
    for the prediction of the next item in the sequence based on prior data.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __build_markov_model(s: str) -> typing.Dict[str, typing.Dict[str, int]]:
        import re

        graph: typing.Dict[str, typing.Dict[str, int]] = {}

        list_of_list_of_words: typing.List[typing.List[str]] = [
            re.findall(r"\w+|[^\w\s]", s)
            for s in MarkovModelGenerator.__extract_simple_sentences(s)
        ]
        for list_of_words in list_of_list_of_words:

            # add start to model
            for c in ".?!":
                if c not in graph:
                    graph[c] = {}
                graph[c][list_of_words[0]] = graph[c].get(list_of_words[0], 0) + 1

            # add sentence to model
            for i in range(1, len(list_of_words)):
                w0: str = list_of_words[i - 1]
                w1: str = list_of_words[i]
                if w0 not in graph:
                    graph[w0] = {}
                graph[w0][w1] = graph[w0].get(w1, 0) + 1

        # return
        return graph

    @staticmethod
    def __extract_simple_sentences(s: str) -> typing.List[str]:
        import re

        s0 = re.findall(
            r"([A-Z][A-Za-z\s]+[.!?])(\s[A-Z][A-Za-z\s]+[.!?])(\s[A-Z][A-Za-z\s]+[.!?])",
            s,
        )
        s1 = []
        for i in range(1, len(s0) - 1):
            if len(s0[i][0]) < 16:
                continue
            if len(s0[i][1]) < 16:
                continue
            if len(s0[i][2]) < 16:
                continue
            s1 += [re.sub("\\s+", " ", s0[i][1])]
        return s1

    #
    # PUBLIC
    #

    @staticmethod
    def build_compressed_markov_model(
        project_gutenberg_urls: typing.List[str],
    ) -> bytes:
        """
        Build and compress a Markov model from a list of Project Gutenberg URLs.

        This method constructs a Markov model from the text of the provided
        Project Gutenberg URLs and compresses the resulting model using zlib
        compression at the highest compression level (9). The compressed model
        is returned as a byte string, which is useful for efficient storage or
        transmission.

        :param project_gutenberg_urls:  A list of URLs pointing to Project Gutenberg texts.
        :return:                        A byte string containing the compressed Markov model.
        """
        import json
        import zlib

        return zlib.compress(
            json.dumps(
                MarkovModelGenerator.build_markov_model(project_gutenberg_urls)
            ).encode(),
            level=9,
        )

    @staticmethod
    def build_markov_model(
        project_gutenberg_urls: typing.List[str],
    ) -> typing.Dict[str, typing.Dict[str, int]]:
        """
        Build a Markov model from a list of Project Gutenberg URLs.

        This method downloads text from the provided Project Gutenberg URLs and
        constructs a Markov model based on the word transitions in the text. The
        model is represented as a dictionary where each key is a word, and the
        value is another dictionary that maps subsequent words to their frequency.

        :param project_gutenberg_urls:  A list of URLs pointing to Project Gutenberg texts.
        :return:                        Dict[str, Dict[str, int]]: A nested dictionary representing the
                                        Markov model. The outer dictionary maps a word to another dictionary,
                                        which maps subsequent words to their occurrence counts.
        """
        # WGET all text
        try:
            import requests  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Please install the 'requests' library to use the MarkovModelGenerator class. "
                "You can install it with 'pip install requests'."
            )

        text: str = ""
        for url in project_gutenberg_urls:
            text += requests.get(url).text

        # build MM
        return MarkovModelGenerator.__build_markov_model(text)
