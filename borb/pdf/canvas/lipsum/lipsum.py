#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
    when an unknown printer took a galley of type and scrambled it to make a type specimen book.
    It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
    It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
    and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""

import random
import pathlib
from borb.pdf.canvas.lipsum.text_generator import TextGenerator


class Lipsum:
    """
    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
    when an unknown printer took a galley of type and scrambled it to make a type specimen book.
    It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
    It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
    and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def generate_agatha_christie_text(number_of_sentences: int = 5) -> str:
        """
        This function produces Agatha Christie styled lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(
            resources_dir / "mm_agatha_christie.json"
        )
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )

    @staticmethod
    def generate_alan_alexander_milne_text(number_of_sentences: int = 5) -> str:
        """
        This function produces A.A. Milne styled lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(
            resources_dir / "mm_alan_alexander_milne.json"
        )
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )

    @staticmethod
    def generate_arthur_conan_doyle_text(number_of_sentences: int = 5) -> str:
        """
        This function produces Arthur Conan Doyle styled lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(
            resources_dir / "mm_arthur_conan_doyle.json"
        )
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )

    @staticmethod
    def generate_emily_bronte_text(number_of_sentences: int = 5) -> str:
        """
        This function produces Emily Brontë styled lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(resources_dir / "mm_emily_bronte.json")
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )

    @staticmethod
    def generate_jane_austen_text(number_of_sentences: int = 5) -> str:
        """
        This function produces Jane Austen styled lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(resources_dir / "mm_jane_austen.json")
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )

    @staticmethod
    def generate_lewis_carroll_text(number_of_sentences: int = 5) -> str:
        """
        This function produces Lewis Carroll styled lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(
            resources_dir / "mm_lewis_carroll.json"
        )
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )

    @staticmethod
    def generate_lipsum_text(number_of_sentences: int = 5) -> str:
        """
        This function produces lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :param start_with_lorem_ipsum:      whether or not to start the text with "Lorem ipsum"
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(resources_dir / "mm_lipsum.json")
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )

    @staticmethod
    def generate_mary_shelley_text(number_of_sentences: int = 5) -> str:
        """
        This function produces Mary Shelley styled lorem ipsum text
        :param number_of_sentences:         the number of sentences to be produced
        :return:                            lorem ipsum text
        """
        assert (
            number_of_sentences >= 1
        ), "number_of_sentences must be a positive non-zero quantity"
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        tg: TextGenerator = TextGenerator().load(resources_dir / "mm_mary_shelley.json")
        return "".join(
            [
                tg.generate(random.randint(7, 32)) + " "
                for _ in range(0, number_of_sentences)
            ]
        )
