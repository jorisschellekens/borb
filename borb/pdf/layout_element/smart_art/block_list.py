#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class representing a simple, structured list layout where each item is displayed as a block element.

The `BasicBlockList` class is designed to arrange items in a sequential block format, providing a straightforward
way to display a list of items where each entry is visually separated for clarity. This layout is ideal for
creating organized lists of information, such as feature highlights, bullet points, or structured content sections.

This layout can be customized with various styles to control text, background colors, and spacing between blocks,
allowing it to adapt to diverse document layouts and visual themes.
"""
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.space.space import Space
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class BasicBlockList:
    """
    A class representing a simple, structured list layout where each item is displayed as a block element.

    The `BasicBlockList` class is designed to arrange items in a sequential block format, providing a straightforward
    way to display a list of items where each entry is visually separated for clarity. This layout is ideal for
    creating organized lists of information, such as feature highlights, bullet points, or structured content sections.

    This layout can be customized with various styles to control text, background colors, and spacing between blocks,
    allowing it to adapt to diverse document layouts and visual themes.
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
        Construct a Basic Block List layout element with specified attributes.

        This static method creates a visually appealing block list structure
        suitable for use in smart art representations. It allows customization
        of the background color, font color, and font size for the level 1 items.

        :params: level_1_items: A list of strings representing the items to be displayed as the first level in the block list.
        :params: background_color: The background color of the block list. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the level 1 items. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the level 1 items. Defaults to 12.

        :returns:   An instance representing the constructed block list layout element,
                    which can be used for further rendering or manipulation.
        """
        # set up table
        n: int = math.ceil(len(level_1_items) ** 0.5)
        m: int = math.ceil(len(level_1_items) / n)
        t: Table = FlexibleColumnWidthTable(
            number_of_rows=m + (m - 1), number_of_columns=n + (n - 1)
        )

        # fill table
        for i in range(0, len(level_1_items)):
            t.append_layout_element(
                Table.TableCell(
                    Paragraph(
                        level_1_items[i],
                        text_alignment=LayoutElement.TextAlignment.CENTERED,
                        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                        font_color=level_1_font_color,
                        font_size=level_1_font_size,
                    ),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    border_color=background_color,
                    background_color=background_color,
                    padding_bottom=level_1_font_size,
                    padding_left=level_1_font_size,
                    padding_right=level_1_font_size,
                    padding_top=level_1_font_size,
                )
            )
            if (i % n) < n - 1:
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        padding_left=level_1_font_size // 2,
                        padding_right=level_1_font_size // 2,
                        border_width_bottom=0,
                        border_width_left=0,
                        border_width_right=0,
                        border_width_top=0,
                    )
                )
            if (i % n) == n - 1 and i != len(level_1_items) - 1:
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        padding_left=level_1_font_size // 2,
                        padding_right=level_1_font_size // 2,
                        column_span=n + (n - 1),
                        border_width_bottom=0,
                        border_width_left=0,
                        border_width_right=0,
                        border_width_top=0,
                    )
                )

        # return
        return t
