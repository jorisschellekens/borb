#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class representing a vertical list layout where each item contains an image paired with optional descriptive text.

The `VerticalPictureList` class is designed to arrange items in a vertically stacked format, ideal for creating
visually organized lists that combine images and text in a structured, sequential display. It is commonly used in
documents, presentations, and other visual media where a clean, vertical alignment is desired.

This layout provides a visually consistent format for showcasing collections of items such as portfolios, catalogs,
team profiles, or any content that benefits from a vertical arrangement of image-text combinations.
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


class VerticalPictureList:
    """
    A class representing a vertical list layout where each item contains an image paired with optional descriptive text.

    The `VerticalPictureList` class is designed to arrange items in a vertically stacked format, ideal for creating
    visually organized lists that combine images and text in a structured, sequential display. It is commonly used in
    documents, presentations, and other visual media where a clean, vertical alignment is desired.

    This layout provides a visually consistent format for showcasing collections of items such as portfolios, catalogs,
    team profiles, or any content that benefits from a vertical arrangement of image-text combinations.
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
        Construct a vertical list layout element containing paired items with hierarchical text levels and images.

        This method builds a visual element that organizes `level_1_items` in a primary list format, where each main item
        is accompanied by a list of sub-items (`level_2_items`) and an associated image. It supports customization of
        text and background colors, font sizes, and image sizing for tailored styling.

        :param level_1_items:       Primary text items to be displayed at the top level in the vertical list.
        :param level_2_items:       A list of lists, where each sublist contains secondary text items related to each corresponding `level_1_item`. Each sublist aligns with the hierarchy of the primary items.
        :param pictures:            Paths to images that will accompany each primary item. The length should match `level_1_items` for consistent pairing.
        :param background_color:    Background color of the layout. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color:  Font color for `level_1_items`. Defaults to `X11Color.WHITE`.
        :param level_1_font_size:   Font size for `level_1_items`. Defaults to 16.
        :param level_2_font_color:  Font color for `level_2_items`. Defaults to `X11Color.WHITE`.
        :param level_2_font_size:   Font size for `level_2_items`. Defaults to 14.
        :param picture_size:        Width and height for each picture in pixels. Defaults to (128, 128).

        :return: A layout element object representing the vertically aligned list with hierarchical text and image elements.
        """
        n: int = len(pictures)
        t: Table = FlexibleColumnWidthTable(
            number_of_rows=n * 2 + (n - 1), number_of_columns=2
        )
        for i, picture, level_1, level_2 in zip(
            range(0, n), pictures, level_1_items, level_2_items
        ):
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
            if i < n - 1:
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        column_span=2,
                        border_width_bottom=0,
                        border_width_left=0,
                        border_width_right=0,
                        border_width_top=0,
                    )
                )
        return t
