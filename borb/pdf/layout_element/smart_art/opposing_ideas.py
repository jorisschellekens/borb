#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a layout for visually contrasting two opposing ideas or concepts, with directional arrows emphasizing the contrast.

This class arranges items in two levels, where each level represents one side
of the opposing ideas. The layout consists of an "arrow down" symbol pointing
to the first level of items, and an "arrow up" symbol pointing to the second
level. This structure highlights differences or opposing perspectives between
the two levels, making it ideal for comparing concepts, options, pros and cons,
or other dual aspects.
"""

import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class OpposingIdeas:
    """
    Represents a layout for visually contrasting two opposing ideas or concepts, with directional arrows emphasizing the contrast.

    This class arranges items in two levels, where each level represents one side
    of the opposing ideas. The layout consists of an "arrow down" symbol pointing
    to the first level of items, and an "arrow up" symbol pointing to the second
    level. This structure highlights differences or opposing perspectives between
    the two levels, making it ideal for comparing concepts, options, pros and cons,
    or other dual aspects.
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
        Construct an "opposing ideas" layout, visually contrasting two sets of ideas with directional arrows emphasizing the distinction.

        This static method arranges items in two levels to visually represent
        opposing concepts or ideas. Each item in `level_1_items` corresponds to
        an item in `level_2_items`, with an arrow pointing down towards the
        first level and an arrow pointing up towards the second, emphasizing
        the contrast between the two. Customization options for colors and
        font sizes allow for adapting the layout to different visual themes.

        :param level_1_items: A list of strings representing the first set of items or ideas (Level 1).
        :param level_2_items: A list of lists, where each sub-list contains strings for the corresponding items in the second set (Level 2).
        :param background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color: The font color for Level 1 items. Defaults to X11Color.WHITE.
        :param level_1_font_size: The font size for Level 1 items. Defaults to 16.
        :param level_2_font_color: The font color for Level 2 items. Defaults to X11Color.WHITE.
        :param level_2_font_size: The font size for Level 2 items. Defaults to 14.
        :return: A LayoutElement representing the constructed "opposing ideas" layout, suitable for rendering in a graphical interface.
        """
        # create a (much) lighter background color
        lighter_background_color = background_color
        for _ in range(0, 5):
            lighter_background_color = lighter_background_color.lighter()

        # set up table
        n = len(level_1_items)
        t = FlexibleColumnWidthTable(number_of_rows=2, number_of_columns=4)

        # arrow down
        arrow_down = LineArt.arrow_down(
            line_width=1,
            fill_color=lighter_background_color,
            stroke_color=lighter_background_color,
        ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
        # fmt: off
        arrow_down._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
        arrow_down._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
        # fmt: on
        t.append_layout_element(
            Table.TableCell(
                arrow_down,
                row_span=2,
                padding_left=level_1_font_size // 2,
                padding_right=level_1_font_size // 2,
                border_width_bottom=0,
                border_width_left=0,
                border_width_right=0,
                border_width_top=0,
            )
        )

        # level 1
        for color, level_1 in zip(
            [lighter_background_color, background_color], level_1_items
        ):
            t.append_layout_element(
                Table.TableCell(
                    Paragraph(
                        level_1,
                        font_size=level_1_font_size,
                        font_color=level_1_font_color,
                        font=Standard14Fonts.get("Helvetica-bold"),
                    ),
                    background_color=color,
                    border_color=color,
                    padding_bottom=level_2_font_size,
                    padding_left=level_2_font_size,
                    padding_right=level_2_font_size,
                    padding_top=level_2_font_size,
                )
            )

        # arrow up
        arrow_up = LineArt.arrow_up(
            line_width=1,
            fill_color=background_color,
            stroke_color=background_color,
        ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
        # fmt: off
        arrow_up._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
        arrow_up._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
        # fmt: on
        t.append_layout_element(
            Table.TableCell(
                arrow_up,
                row_span=2,
                padding_left=level_1_font_size // 2,
                padding_right=level_1_font_size // 2,
                border_width_bottom=0,
                border_width_left=0,
                border_width_right=0,
                border_width_top=0,
            )
        )

        # add level_2
        for color, level_2 in zip(
            [lighter_background_color, background_color], level_2_items
        ):
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
                    border_color=color,
                    background_color=color,
                    padding_bottom=level_2_font_size,
                    padding_left=level_2_font_size,
                    padding_right=level_2_font_size,
                    padding_top=level_2_font_size,
                )
            )

        # return
        return t
