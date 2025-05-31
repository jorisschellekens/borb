#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a horizontal layout for visualizing a process with steps, each accompanied by a pie chart that indicates progress.

This class allows the creation of a clear representation of a multistep
process, where each step is visually marked and supplemented by a pie
chart reflecting the percentage of completion. The first step begins with
an empty pie chart, while subsequent steps can show varying levels of
progress, such as 50% for the second step and 100% for the final step.
This intuitive layout aids in understanding the flow and status of the
overall process at a glance.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.space.space import Space
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class HorizontalPieProcess:
    """
    Represents a horizontal layout for visualizing a process with steps, each accompanied by a pie chart that indicates progress.

    This class allows the creation of a clear representation of a multistep
    process, where each step is visually marked and supplemented by a pie
    chart reflecting the percentage of completion. The first step begins with
    an empty pie chart, while subsequent steps can show varying levels of
    progress, such as 50% for the second step and 100% for the final step.
    This intuitive layout aids in understanding the flow and status of the
    overall process at a glance.
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
        Construct a horizontal process layout with steps, each accompanied by a pie chart indicating progress.

        This static method builds a visual representation of a multistep
        process. Each step (level 1 item) is displayed alongside a corresponding
        set of details (level 2 items) and a pie chart that illustrates the
        progress for that step. The method allows customization of background
        color, font colors, and font sizes for both levels, providing a clear
        and aesthetically pleasing layout.

        :params: level_1_items:         A list of strings representing the main steps in the process.
        :params: level_2_items:         A list of lists, where each sub-list contains strings providing additional details or sub-steps related to each main step.
        :params: background_color:      The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color:    The font color for the main step items. Defaults to X11Color.WHITE.
        :params: level_1_font_size:     The font size for the main step items. Defaults to 16.
        :params: level_2_font_color:    The font color for the sub-step items. Defaults to X11Color.WHITE.
        :params: level_2_font_size:     The font size for the sub-step items. Defaults to 14.
        :returns:                       A LayoutElement representing the constructed horizontal process layout, suitable for rendering in a graphical interface.
        """
        # create a (much) lighter background color
        lighter_background_color = background_color
        for _ in range(0, 5):
            lighter_background_color = lighter_background_color.lighter()

        # set up table
        n = len(level_1_items)
        t = FlexibleColumnWidthTable(
            number_of_rows=2, number_of_columns=n * 2 + (n - 1)
        )

        # fill table
        for i, level_1 in enumerate(level_1_items):

            # IF we are at 0%
            # THEN draw a special shape (empty circle)
            p: int = (360 * i) // (n - 1)
            if p == 0:
                t.append_layout_element(
                    Table.TableCell(
                        LineArt.circle(
                            stroke_color=level_1_font_color,
                            line_width=level_2_font_size // 3,
                            fill_color=None,
                        ).scale_to_fit(
                            size=(level_1_font_size * 3, level_1_font_size * 3)
                        ),
                        background_color=background_color,
                        border_color=background_color,
                        padding_bottom=level_2_font_size,
                        padding_left=level_2_font_size,
                        padding_right=level_2_font_size,
                        padding_top=level_2_font_size,
                    )
                )
            # IF we are not at 0%
            # THEN fill the circle gradually
            else:
                t.append_layout_element(
                    Table.TableCell(
                        LineArt.fraction_of_circle(
                            angle_in_degrees=p,
                            stroke_color=level_1_font_color,
                            fill_color=level_1_font_color,
                        ).scale_to_fit(
                            size=(level_1_font_size * 3, level_1_font_size * 3)
                        ),
                        background_color=background_color,
                        border_color=background_color,
                        padding_right=level_2_font_size,
                        padding_bottom=level_2_font_size,
                        padding_left=level_2_font_size,
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
                        padding_top=level_2_font_size,
                    ),
                    background_color=background_color,
                    border_color=background_color,
                    padding_right=level_2_font_size,
                )
            )
            # add margin
            if i != n - 1:
                t.append_layout_element(
                    Table.TableCell(
                        Space(size=(level_1_font_size, level_1_font_size)),
                        padding_left=level_2_font_size // 2,
                        padding_right=level_2_font_size // 2,
                        row_span=2,
                        border_width_bottom=0,
                        border_width_left=0,
                        border_width_right=0,
                        border_width_top=0,
                    )
                )

        # add lists
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
                    column_span=2,
                    background_color=lighter_background_color,
                    border_color=lighter_background_color,
                    padding_bottom=level_2_font_size,
                    padding_left=level_2_font_size,
                    padding_right=level_2_font_size,
                    padding_top=level_2_font_size,
                )
            )

        # return
        return t
