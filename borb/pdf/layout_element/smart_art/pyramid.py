#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a pyramid layout that visually organizes a series of items in a hierarchical structure, with each level displayed as a centered row.

This class is designed to create a structured pyramid presentation where
items are displayed in rows that progressively grow wider toward the base.
The layout allows customization of colors, font size, and alignment to
enhance the visual appeal and readability. The pyramid format is ideal
for illustrating concepts such as hierarchy, priorities, or layered
structures in workflows, processes, or data presentations.
"""
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


class Pyramid:
    """
    Represents a pyramid layout that visually organizes a series of items in a hierarchical structure, with each level displayed as a centered row.

    This class is designed to create a structured pyramid presentation where
    items are displayed in rows that progressively grow wider toward the base.
    The layout allows customization of colors, font size, and alignment to
    enhance the visual appeal and readability. The pyramid format is ideal
    for illustrating concepts such as hierarchy, priorities, or layered
    structures in workflows, processes, or data presentations.
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
        Build a pyramid layout as a `LayoutElement` with the given items and appearance settings.

        This method creates a hierarchical pyramid structure where each item is displayed
        in a centered row. The rows are progressively wider toward the base, forming the
        shape of a pyramid. The visual appearance can be customized with parameters
        such as background color, font color, and font size.

        :param level_1_items: A list of strings representing the items to include in the pyramid. Each string corresponds to a row, starting from the top.
        :param background_color: The background color for the pyramid rows. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color: The font color for the text in the pyramid. Defaults to `X11Color.WHITE`.
        :param level_1_font_size: The font size for the text in the pyramid. Defaults to `12`.

        :return: A `LayoutElement` representing the pyramid structure, ready to be added to a PDF.
        """
        light_background_color: Color = background_color
        for _ in range(0, 5):
            light_background_color = light_background_color.lighter()
        n: int = len(level_1_items)
        m: int = (len(level_1_items) - 1) * 2 + 1
        t: Table = FlexibleColumnWidthTable(
            number_of_rows=n + (n - 1), number_of_columns=m
        )
        for row_index, level_1_item in enumerate(level_1_items):
            span1: int = row_index * 2 + 1
            span0: int = (m - span1) // 2
            for i in range(0, span0):
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        border_width_top=0,
                        border_width_right=0,
                        border_width_bottom=0,
                        border_width_left=0,
                    )
                )
            t.append_layout_element(
                Table.TableCell(
                    Paragraph(
                        level_1_item,
                        font_color=level_1_font_color,
                        font_size=level_1_font_size,
                        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                        text_alignment=LayoutElement.TextAlignment.CENTERED,
                    ),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    border_color=light_background_color,
                    background_color=background_color,
                    padding_top=level_1_font_size // 2,
                    padding_right=level_1_font_size // 2,
                    padding_bottom=level_1_font_size // 2,
                    padding_left=level_1_font_size // 2,
                    column_span=span1,
                )
            )
            for i in range(0, span0):
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        border_width_top=0,
                        border_width_right=0,
                        border_width_bottom=0,
                        border_width_left=0,
                    )
                )
            if row_index < n - 1:
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        padding_top=level_1_font_size // 2,
                        column_span=m,
                        border_width_top=0,
                        border_width_right=0,
                        border_width_bottom=0,
                        border_width_left=0,
                    )
                )
        return t
