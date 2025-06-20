#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a horizontal process layout that visually organizes a series of items as blocks connected by arrows, illustrating the flow of a process.

This class is designed to create a structured representation of a process,
where each item in the process is displayed as a block. Arrows connect
these blocks, indicating the sequence and direction of the process flow.
This layout is particularly useful for visualizing workflows, project
steps, or any sequential operations.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class HorizontalProcess:
    """
    Represents a horizontal process layout that visually organizes a series of items as blocks connected by arrows, illustrating the flow of a process.

    This class is designed to create a structured representation of a process,
    where each item in the process is displayed as a block. Arrows connect
    these blocks, indicating the sequence and direction of the process flow.
    This layout is particularly useful for visualizing workflows, project
    steps, or any sequential operations.
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
        Construct a horizontal process layout with items represented as blocks connected by arrows.

        This static method creates a visual representation of a series of items
        in a process, where each item (level 1) is displayed as a block.
        The blocks are connected by arrows to illustrate the flow of the process.
        Users can customize the background color, font color, and font size
        for the block labels, allowing for a tailored appearance.

        :params: level_1_items: A list of strings representing the items in the process.
        :params: background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the block labels. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the block labels. Defaults to 12.
        :returns: A LayoutElement representing the constructed horizontal process layout, suitable for rendering.
        """
        # create a (much) lighter background color
        lighter_background_color = background_color
        for _ in range(0, 5):
            lighter_background_color = lighter_background_color.lighter()

        # set up table
        n: int = len(level_1_items)
        t: Table = FlexibleColumnWidthTable(
            number_of_columns=n + (n - 1), number_of_rows=1
        )

        # fill table
        for i, level_1 in enumerate(level_1_items):
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
            if i != n - 1:
                arrow = LineArt.arrow_right(
                    line_width=1,
                    fill_color=lighter_background_color,
                    stroke_color=lighter_background_color,
                ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
                # fmt: off
                arrow._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
                arrow._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
                # fmt: on
                t.append_layout_element(
                    Table.TableCell(
                        arrow,
                        padding_left=level_1_font_size // 2,
                        padding_right=level_1_font_size // 2,
                        border_width_bottom=0,
                        border_width_left=0,
                        border_width_right=0,
                        border_width_top=0,
                    )
                )

        # return
        return t
