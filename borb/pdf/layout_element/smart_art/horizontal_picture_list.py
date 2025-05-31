#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class representing a horizontal list layout where each item contains an image and optional text, arranged in a horizontal row.

The `HorizontalPictureList` class is designed to create a horizontally aligned list of items, with each item
displaying a picture and accompanying text. This layout is useful for document generation, presentations, or
visual media where horizontally structured image-text pairs are required, such as in product showcases, galleries,
or team member profiles.

This layout provides a visually cohesive format for presenting collections of items in a left-to-right arrangement,
ideal for content that benefits from a compact horizontal design.
"""

import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.space.space import Space
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class HorizontalPictureList:
    """
    A class representing a horizontal list layout where each item contains an image and optional text, arranged in a horizontal row.

    The `HorizontalPictureList` class is designed to create a horizontally aligned list of items, with each item
    displaying a picture and accompanying text. This layout is useful for document generation, presentations, or
    visual media where horizontally structured image-text pairs are required, such as in product showcases, galleries,
    or team member profiles.

    This layout provides a visually cohesive format for presenting collections of items in a left-to-right arrangement,
    ideal for content that benefits from a compact horizontal design.
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
        level_2_items: typing.List[typing.List[str]],
        pictures: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
        picture_size: typing.Tuple[int, int] = (128, 128),
    ) -> LayoutElement:
        """
        Construct a horizontal list layout element containing paired items with hierarchical text levels and images.

        This method arranges `level_1_items` in a horizontal row, where each main item is paired with a list of sub-items
        (`level_2_items`) and an associated image. Each item can be customized with specific colors, font sizes,
        and image dimensions to create a visually cohesive horizontal list.

        :param level_1_items: Primary text items to be displayed at the top level in the horizontal list.
        :param level_2_items: A list of lists, where each sublist contains secondary text items related to each corresponding item in `level_1_items`. Each sublist aligns with the structure of `level_1_items`.
        :param pictures: Paths to images that accompany each primary item. The length should match `level_1_items` for consistent pairing.
        :param background_color: Background color of the layout. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color: Font color for `level_1_items`. Defaults to `X11Color.WHITE`.
        :param level_1_font_size: Font size for `level_1_items`. Defaults to 16.
        :param level_2_font_color: Font color for `level_2_items`. Defaults to `X11Color.WHITE`.
        :param level_2_font_size: Font size for `level_2_items`. Defaults to 14.
        :param picture_size: Dimensions of each picture in pixels, as (width, height). Defaults to (128, 128).

        :return: A layout element representing the horizontally aligned list with hierarchical text and image elements.
        """
        # set up table
        n: int = len(pictures)
        t: Table = FlexibleColumnWidthTable(
            number_of_rows=2, number_of_columns=n * 2 + (n - 1)
        )

        # fill table
        for i, picture, level_1 in zip(range(0, n), pictures, level_1_items):
            t.append_layout_element(
                Table.TableCell(
                    Image(picture, size=picture_size),
                    border_color=background_color,
                    background_color=background_color,
                    row_span=2,
                    padding_bottom=level_2_font_size,
                    padding_left=level_2_font_size,
                    padding_right=level_2_font_size,
                    padding_top=level_2_font_size,
                )
            )
            t.append_layout_element(
                Table.TableCell(
                    Paragraph(
                        level_1,
                        font_size=level_1_font_size,
                        font_color=level_1_font_color,
                        font=Standard14Fonts.get("Helvetica-bold"),
                    ),
                    background_color=background_color,
                    border_color=background_color,
                    padding_bottom=level_2_font_size,
                    padding_left=level_2_font_size,
                    padding_right=level_2_font_size,
                    padding_top=level_2_font_size,
                )
            )
            if i < n - 1:
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        row_span=2,
                        border_width_top=0,
                        border_width_bottom=0,
                        border_width_left=0,
                        border_width_right=0,
                        padding_left=level_2_font_size // 2,
                        padding_right=level_2_font_size // 2,
                    )
                )
        for level_2 in level_2_items:
            ul: UnorderedList = UnorderedList()
            for item in level_2:
                ul.append_layout_element(
                    Paragraph(
                        item,
                        font_size=level_2_font_size,
                        font_color=level_2_font_color,
                    )
                )
            t.append_layout_element(
                Table.TableCell(
                    ul,
                    border_color=background_color,
                    background_color=background_color,
                    padding_bottom=level_2_font_size,
                    padding_left=level_2_font_size,
                    padding_right=level_2_font_size,
                    padding_top=level_2_font_size,
                )
            )

        # return
        return t
