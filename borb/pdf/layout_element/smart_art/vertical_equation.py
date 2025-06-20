#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a vertical equation layout that displays a preset equation format: "A + B + C ... = D".

This class provides a visual layout specifically designed to represent
an equation in which the components "A", "B", "C", etc., are user-defined
inputs, while the operators "+" and "=" remain fixed. Users can configure
the items on either side of the equation, but cannot change the equation
structure or operators.

The layout is ideal for scenarios where specific inputs need to be summed
or combined to produce a result, and is commonly used in educational,
financial, or analytical presentations. Customization options are available
for background color, font colors, and font sizes for each component,
allowing for visual adaptation to fit specific themes or presentation needs.
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


class VerticalEquation:
    """
    Represents a vertical equation layout that displays a preset equation format: "A + B + C ... = D".

    This class provides a visual layout specifically designed to represent
    an equation in which the components "A", "B", "C", etc., are user-defined
    inputs, while the operators "+" and "=" remain fixed. Users can configure
    the items on either side of the equation, but cannot change the equation
    structure or operators.

    The layout is ideal for scenarios where specific inputs need to be summed
    or combined to produce a result, and is commonly used in educational,
    financial, or analytical presentations. Customization options are available
    for background color, font colors, and font sizes for each component,
    allowing for visual adaptation to fit specific themes or presentation needs.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __add_equals(
        level_1_font_size: int, lighter_background_color: Color, table: Table
    ) -> None:
        equals = LineArt.arrow_right(
            line_width=1,
            fill_color=lighter_background_color,
            stroke_color=lighter_background_color,
        ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
        # fmt: off
        equals._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
        equals._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
        # fmt: on
        table.append_layout_element(
            Table.TableCell(
                equals,
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
    def __add_plus(
        level_1_font_size: int, lighter_background_color: Color, table: Table
    ) -> None:
        plus = LineArt.cross(
            line_width=1,
            fill_color=lighter_background_color,
            stroke_color=lighter_background_color,
        ).scale_to_fit(size=(level_1_font_size * 3, level_1_font_size * 3))
        # fmt: off
        plus._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE  # type: ignore[attr-defined]
        plus._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE  # type: ignore[attr-defined]
        # fmt: on
        table.append_layout_element(
            Table.TableCell(
                plus,
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
    def __add_text_block(
        background_color: Color,
        level_1: str,
        level_1_font_color: Color,
        level_1_font_size: int,
        table: Table,
    ) -> None:
        table.append_layout_element(
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
        Construct a vertical equation layout displaying a fixed format equation: "A + B + C ... = D".

        This method arranges items horizontally in a predetermined equation
        structure, where each item in `level_1_items` is displayed sequentially
        as terms (A, B, C, etc.) on the left side of a "+" operation, culminating
        in an "=" operation leading to the final result. The "+" and "=" operators
        are fixed and cannot be modified. Customization options for background
        color, font color, and font size allow the equation's appearance to be
        tailored as needed.

        :param level_1_items:       A list of strings representing the items to be  included in the equation, where each item will represent a term of the equation.
        :param background_color:    The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color:  The font color for the equation terms. Defaults to X11Color.WHITE.
        :param level_1_font_size:   The font size for the equation terms. Defaults to 12.
        :return:                    A LayoutElement representing the horizontal equation layout, ready for rendering with a fixed structure showing "A + B + C ... = D".
        """
        # create a (much) lighter background color
        lighter_background_color = background_color
        for _ in range(0, 5):
            lighter_background_color = lighter_background_color.lighter()

        # set up table
        n: int = len(level_1_items)
        k = ((n - 1) + (n - 2)) // 2
        t: Table = FlexibleColumnWidthTable(
            number_of_columns=3, number_of_rows=(n - 1) + (n - 2)
        )
        for i in range(0, (n - 1) + (n - 2)):
            if i % 2 == 0:
                VerticalEquation.__add_text_block(
                    background_color,
                    level_1_items[i // 2],
                    level_1_font_color,
                    level_1_font_size,
                    t,
                )
            else:
                VerticalEquation.__add_plus(
                    level_1_font_size, lighter_background_color, t
                )

            if i == k:
                VerticalEquation.__add_equals(
                    level_1_font_size, lighter_background_color, t
                )
                VerticalEquation.__add_text_block(
                    background_color,
                    level_1_items[-1],
                    level_1_font_color,
                    level_1_font_size,
                    t,
                )

            else:
                t.append_layout_element(Paragraph("", font_size=level_1_font_size))
                t.append_layout_element(Paragraph("", font_size=level_1_font_size))

        # return
        return t.no_borders()
