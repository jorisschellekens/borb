#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class providing an aesthetically pleasing way to represent a list of string objects (tags) on the pages of a PDF.

The `Tags` class is designed to visually format and arrange tags, such as skills, interests, or keywords,
in a coherent and appealing layout. Each tag is styled with customizable colors, font sizes, and padding,
making it suitable for use in documents like resumes, portfolios, or brochures.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph


class Tags:
    """
    A class providing an aesthetically pleasing way to represent a list of string objects (tags) on the pages of a PDF.

    The `Tags` class is designed to visually format and arrange tags, such as skills, interests, or keywords,
    in a coherent and appealing layout. Each tag is styled with customizable colors, font sizes, and padding,
    making it suitable for use in documents like resumes, portfolios, or brochures.
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
    def build(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Build a layout element representing the collection of tags.

        This method constructs a visual representation of the tags as a paragraph, with each tag styled
        using the specified background color, font color, and font size. Tags are separated by underscores.

        :param level_1_items: A list of strings representing the tags to display.
        :param background_color: The background color for the tags. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color: The font color for the tags. Defaults to `X11Color.WHITE`.
        :param level_1_font_size: The font size for the tags. Defaults to 12.
        :return: A `LayoutElement` representing the formatted tags.
        """
        chunks: typing.List[Chunk] = []
        for x in level_1_items:
            chunks += [
                Chunk(
                    x,
                    font_color=level_1_font_color,
                    font_size=level_1_font_size,
                    background_color=background_color,
                    padding_bottom=level_1_font_size // 4,
                    padding_left=level_1_font_size // 4,
                    padding_right=level_1_font_size // 4,
                )
            ]
            chunks += [
                Chunk("_", font_color=level_1_font_color, font_size=level_1_font_size)
            ]

        return HeterogeneousParagraph(chunks=chunks)
