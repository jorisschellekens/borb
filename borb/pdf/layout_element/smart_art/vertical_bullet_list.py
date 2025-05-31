#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a vertical bullet list layout element for displaying items in a visually appealing, bullet-point format.

This class is designed to create and manage a vertical list of items,
each preceded by a bullet symbol. It allows customization of bullet styles,
spacing, and colors to enhance the visual presentation of the list.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.space.space import Space
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class VerticalBulletList:
    """
    Represents a vertical bullet list layout element for displaying items in a visually appealing, bullet-point format.

    This class is designed to create and manage a vertical list of items,
    each preceded by a bullet symbol. It allows customization of bullet styles,
    spacing, and colors to enhance the visual presentation of the list.
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
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
    ) -> LayoutElement:
        """
        Construct a vertical bullet list layout element with specified attributes for multiple levels of items.

        This static method creates a structured horizontal bullet list where
        the first level contains primary items and the second level contains
        sub-items for each primary item. It allows for customization of
        background colors, font colors, and font sizes for both levels.

        :params: level_1_items: A list of strings representing the primary items in the bullet list.
        :params: level_2_items: A list of lists, where each sub-list contains strings representing the sub-items corresponding to the primary items.
        :params: background_color: The background color of the bullet list. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the primary items. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the primary items. Defaults to 16.
        :params: level_2_font_color: The font color for the sub-items. Defaults to X11Color.WHITE.
        :params: level_2_font_size: The font size for the sub-items. Defaults to 14.

        :returns: A LayoutElement representing the constructed vertical bullet list layout, suitable for rendering in a graphical interface.
        """
        # create a (much) lighter background color
        lighter_background_color = background_color
        for _ in range(0, 5):
            lighter_background_color = lighter_background_color.lighter()

        # set up table
        n: int = len(level_1_items)
        t: Table = FlexibleColumnWidthTable(
            number_of_rows=n * 2 + (n - 1), number_of_columns=1
        )

        # fill table
        for i, level_1, level_2 in zip(range(0, n), level_1_items, level_2_items):
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
                    border_color=lighter_background_color,
                    background_color=lighter_background_color,
                    padding_bottom=level_2_font_size,
                    padding_left=level_2_font_size,
                    padding_right=level_2_font_size,
                    padding_top=level_2_font_size,
                )
            )
            if i != (n - 1):
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        padding_left=level_2_font_size // 2,
                        padding_right=level_2_font_size // 2,
                        border_width_bottom=0,
                        border_width_left=0,
                        border_width_right=0,
                        border_width_top=0,
                    )
                )

        # return
        return t
