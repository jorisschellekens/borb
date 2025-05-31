#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a horizontal layout for displaying a list of items in descending order.

This class organizes items horizontally across the display, with each item
progressively descending to illustrate growth, progression, or increasing
importance. The layout provides a visually intuitive way to show sequences
where each item builds on or improves upon the previous one. It is ideal
for representing steps, rankings, achievements, or any process that benefits
from a sense of upward progression.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class HorizontalDescendingList:
    """
    Represents a horizontal layout for displaying a list of items in descending order.

    This class organizes items horizontally across the display, with each item
    progressively descending to illustrate growth, progression, or increasing
    importance. The layout provides a visually intuitive way to show sequences
    where each item builds on or improves upon the previous one. It is ideal
    for representing steps, rankings, achievements, or any process that benefits
    from a sense of upward progression.
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
        Construct a horizontal descending list layout with items displayed in a progressively elevated order.

        This static method creates a visual layout for displaying items
        horizontally, with each item slightly higher than the previous one
        to indicate upward progression. Customization options for background
        color, font color, and font size allow the layout to be adapted to
        specific visual requirements, making it suitable for representing
        ordered steps, rankings, or achievements.

        :param level_1_items: A list of strings representing the items to be displayed in descending order.
        :param background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color: The font color for the item labels. Defaults to X11Color.WHITE.
        :param level_1_font_size: The font size for the item labels. Defaults to 12.
        :return: A LayoutElement representing the constructed horizontal descending list layout, ready for rendering in a graphical interface.
        """
        n: int = len(level_1_items)
        t: Table = FlexibleColumnWidthTable(
            number_of_columns=n, number_of_rows=n + (n - 1)
        )
        for i, level_1 in enumerate(level_1_items):
            x: int = n - i
            y: int = n - x
            t.append_layout_element(
                Table.TableCell(
                    Paragraph(
                        level_1,
                        text_alignment=LayoutElement.TextAlignment.CENTERED,
                        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                        font_color=level_1_font_color,
                        font_size=level_1_font_size,
                    ),
                    border_width_top=0,
                    border_width_right=0,
                    border_width_bottom=0,
                    border_width_left=0,
                    column_span=x,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    border_color=background_color,
                    background_color=background_color,
                    padding_bottom=level_1_font_size,
                    padding_left=level_1_font_size,
                    padding_right=level_1_font_size,
                    padding_top=level_1_font_size,
                )
            )
            if y > 0:
                t.append_layout_element(
                    Table.TableCell(
                        Paragraph("", font_size=level_1_font_size),
                        border_width_top=0,
                        border_width_right=0,
                        border_width_bottom=0,
                        border_width_left=0,
                        column_span=y,
                        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                        padding_bottom=level_1_font_size,
                        padding_left=level_1_font_size,
                        padding_right=level_1_font_size,
                        padding_top=level_1_font_size,
                    )
                )
            # padding
            if i != (n - 1):
                t.append_layout_element(
                    Table.TableCell(
                        Paragraph("", font_size=level_1_font_size),
                        column_span=n,
                        border_width_top=0,
                        border_width_right=0,
                        border_width_bottom=0,
                        border_width_left=0,
                        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                        padding_bottom=level_1_font_size // 2,
                        padding_left=level_1_font_size,
                        padding_right=level_1_font_size,
                        padding_top=level_1_font_size // 2,
                    )
                )
        # return
        return t
