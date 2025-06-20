#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a bending process layout that visually organizes a series of steps or items along a curved path, illustrating the progression of a process.

This class is designed to display items in a curved, flowing layout, which
can help convey movement, transition, or cyclical progression. Each item
represents a step or stage in the process, and the bending layout enhances
the visual appeal by deviating from a traditional straight-line approach.
This format is ideal for workflows, timelines, or processes that benefit
from a dynamic, flowing presentation.
"""
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.space.space import Space
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class BendingProcess:
    """
    Represents a bending process layout that visually organizes a series of steps or items along a curved path, illustrating the progression of a process.

    This class is designed to display items in a curved, flowing layout, which
    can help convey movement, transition, or cyclical progression. Each item
    represents a step or stage in the process, and the bending layout enhances
    the visual appeal by deviating from a traditional straight-line approach.
    This format is ideal for workflows, timelines, or processes that benefit
    from a dynamic, flowing presentation.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __add_arrow_down(
        level_1_font_size: int, lighter_background_color: Color, table: Table
    ):
        arrow = LineArt.arrow_down(
            line_width=1,
            fill_color=lighter_background_color,
            stroke_color=lighter_background_color,
        ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
        # fmt: off
        arrow._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
        arrow._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
        # fmt: on
        table.append_layout_element(
            Table.TableCell(
                arrow,
                padding_top=level_1_font_size // 2,
                padding_bottom=level_1_font_size // 2,
                padding_left=level_1_font_size // 2,
                padding_right=level_1_font_size // 2,
                border_width_bottom=0,
                border_width_left=0,
                border_width_right=0,
                border_width_top=0,
            )
        )

    @staticmethod
    def __add_arrow_left(
        level_1_font_size: int, lighter_background_color: Color, table: Table
    ):
        arrow = LineArt.arrow_left(
            line_width=1,
            fill_color=lighter_background_color,
            stroke_color=lighter_background_color,
        ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
        # fmt: off
        arrow._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
        arrow._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
        # fmt: on
        table.append_layout_element(
            Table.TableCell(
                arrow,
                padding_top=level_1_font_size // 2,
                padding_bottom=level_1_font_size // 2,
                padding_left=level_1_font_size // 2,
                padding_right=level_1_font_size // 2,
                border_width_bottom=0,
                border_width_left=0,
                border_width_right=0,
                border_width_top=0,
            )
        )

    @staticmethod
    def __add_arrow_right(
        level_1_font_size: int, lighter_background_color: Color, table: Table
    ):
        arrow = LineArt.arrow_right(
            line_width=1,
            fill_color=lighter_background_color,
            stroke_color=lighter_background_color,
        ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
        # fmt: off
        arrow._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
        arrow._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
        # fmt: on
        table.append_layout_element(
            Table.TableCell(
                arrow,
                padding_top=level_1_font_size // 2,
                padding_bottom=level_1_font_size // 2,
                padding_left=level_1_font_size // 2,
                padding_right=level_1_font_size // 2,
                border_width_bottom=0,
                border_width_left=0,
                border_width_right=0,
                border_width_top=0,
            )
        )

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
        Construct a bending process layout with items displayed along a curved path.

        This static method creates a visual layout of a process, arranging each
        item (level 1) along a flowing, curved line to convey a sense of progression
        or continuity. Each item appears as a labeled point along the curve,
        and arrows or lines between items indicate the order of the steps.

        :param level_1_items:       A list of strings representing the primary items or steps in the process.
        :param background_color:    The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color:  The font color for item labels. Defaults to X11Color.WHITE.
        :param level_1_font_size:   The font size for item labels. Defaults to 12.
        :returns: A LayoutElement representing the constructed bending process layout, ready for rendering in a graphical interface.
        """
        # create a (much) lighter background color
        lighter_background_color = background_color
        for _ in range(0, 5):
            lighter_background_color = lighter_background_color.lighter()

        # set up table
        n: int = math.ceil(len(level_1_items) ** 0.5)
        m: int = math.ceil(len(level_1_items) / n)
        t: Table = FlexibleColumnWidthTable(
            number_of_rows=m + (m - 1), number_of_columns=n + (n - 1)
        )

        # build a new list of items
        # such that the items can simply be added
        # without having to account for the direction changes
        level_1_items_in_render_order: typing.List[typing.Optional[str]] = []
        left_to_right: bool = False
        for i in range(0, len(level_1_items), n):
            row: typing.List[typing.Optional[str]] = level_1_items[i : i + n]  # type: ignore[assignment]
            row = row + [None for _ in range(0, n - len(row))]
            if left_to_right:
                row = row[::-1]
            level_1_items_in_render_order += row
            left_to_right = not left_to_right

        left_to_right = True
        for i, level_1 in enumerate(level_1_items_in_render_order):

            # IF the content is None
            # THEN do not render anything
            if level_1 is None:
                t.append_layout_element(
                    Space(size=(level_1_font_size, level_1_font_size))
                )

            # IF the content is not None
            # THEN render a block
            else:
                t.append_layout_element(
                    Table.TableCell(
                        Paragraph(
                            level_1,
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

            next_level_1: typing.Optional[str] = (
                level_1_items_in_render_order[i + 1]
                if i + 1 < len(level_1_items_in_render_order)
                else None
            )
            if (i % n) != (n - 1):
                if left_to_right:
                    if level_1 is None or next_level_1 is None:
                        t.append_layout_element(
                            Paragraph("", font_size=level_1_font_size)
                        )
                    else:
                        BendingProcess.__add_arrow_right(
                            level_1_font_size=level_1_font_size,
                            lighter_background_color=lighter_background_color,
                            table=t,
                        )
                else:
                    if level_1 is None or next_level_1 is None:
                        t.append_layout_element(
                            Paragraph("", font_size=level_1_font_size)
                        )
                    else:
                        BendingProcess.__add_arrow_left(
                            level_1_font_size=level_1_font_size,
                            lighter_background_color=lighter_background_color,
                            table=t,
                        )

            has_next_element: bool = i < len(level_1_items) - 1
            if (i % n) == (n - 1) and has_next_element:

                # IF we are going left to right
                # THEN add <empty> <arrow>
                if left_to_right:
                    for _ in range(0, n + n - 2):
                        t.append_layout_element(
                            Paragraph("", font_size=level_1_font_size)
                        )
                    BendingProcess.__add_arrow_down(
                        level_1_font_size=level_1_font_size,
                        lighter_background_color=lighter_background_color,
                        table=t,
                    )

                if not left_to_right:
                    BendingProcess.__add_arrow_down(
                        level_1_font_size=level_1_font_size,
                        lighter_background_color=lighter_background_color,
                        table=t,
                    )
                    for _ in range(0, n + n - 2):
                        t.append_layout_element(
                            Paragraph("", font_size=level_1_font_size)
                        )

                # change direction
                left_to_right = not left_to_right

        # return
        return t.no_borders()
