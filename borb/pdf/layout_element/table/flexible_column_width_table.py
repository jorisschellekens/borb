#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a table with flexible column widths based on the content of its elements.

The `FlexibleColumnWidthTable` class dynamically adjusts the width of each column
according to the size and dimensions of the `LayoutElement` objects inside the table cells.
This allows for flexible and adaptive layouts where the column widths expand or shrink
depending on the content they contain, ensuring that the table remains visually balanced.
"""
import functools
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable


class FlexibleColumnWidthTable(FixedColumnWidthTable):
    """
    Represents a table with flexible column widths based on the content of its elements.

    The `FlexibleColumnWidthTable` class dynamically adjusts the width of each column
    according to the size and dimensions of the `LayoutElement` objects inside the table cells.
    This allows for flexible and adaptive layouts where the column widths expand or shrink
    depending on the content they contain, ensuring that the table remains visually balanced.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a fixed-width table that occupies the full width of the PDF page.

        This constructor allows customization of the table's layout, including its
        number of rows and columns, styling properties like background and border colors,
        and alignment. The `column_widths` parameter defines the width of each column,
        enabling precise control over the table's appearance while ensuring it fills
        the available horizontal space on the page.

        :param number_of_rows:          The total number of rows in the table.
        :param number_of_columns:       The total number of columns in the table.
        :param background_color:        Optional background color for the table.
        :param border_color:            Optional border color for the table.
        :param border_dash_pattern:     Dash pattern used for the border lines of the table.
        :param border_dash_phase:       Phase offset for the dash pattern in the borders.
        :param border_width_bottom:     Width of the bottom border of the table.
        :param border_width_left:       Width of the left border of the table.
        :param border_width_right:      Width of the right border of the table.
        :param border_width_top:        Width of the top border of the table.
        :param horizontal_alignment:     Horizontal alignment of the table (default is LEFT).
        :param margin_bottom:           Space between the table and the element below it.
        :param margin_left:             Space between the table and the left page margin.
        :param margin_right:            Space between the table and the right page margin.
        :param margin_top:              Space between the table and the element above it.
        :param padding_bottom:          Padding inside the table at the bottom.
        :param padding_left:            Padding inside the table on the left side.
        :param padding_right:           Padding inside the table on the right side.
        :param padding_top:             Padding inside the table at the top.
        :param vertical_alignment:       Vertical alignment of the table (default is TOP).
        """
        super().__init__(
            number_of_rows=number_of_rows,
            number_of_columns=number_of_columns,
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    def __calculate_and_set_column_width(
        self, available_space: typing.Tuple[int, int]
    ) -> None:
        # fmt: off
        column_min_widths: typing.List[int] = [max([math.ceil(FlexibleColumnWidthTable.__narrowest_landscape_box(e)[0] / e.get_column_span()) for e in self.get_column(c)]) for c in range(0, self._Table__number_of_columns)]  # type: ignore[attr-defined]
        column_max_widths: typing.List[int] = [max([math.ceil(FlexibleColumnWidthTable.__widest_landscape_box(e)[0] / e.get_column_span()) for e in self.get_column(c)]) for c in range(0, self._Table__number_of_columns)]     # type: ignore[attr-defined]
        # fmt: on

        # fmt: off
        self._FixedColumnWidthTable__column_widths: typing.List[int] = [cw for cw in column_min_widths]
        number_of_expandable_columns: int = sum([1 if cw < cmw else 0 for cw, cmw in zip(self._FixedColumnWidthTable__column_widths, column_max_widths)])
        remaining_width: int = available_space[0] - sum(self._FixedColumnWidthTable__column_widths)
        while remaining_width > 0 and 0 < number_of_expandable_columns <= remaining_width:
            self._FixedColumnWidthTable__column_widths = [(cw + 1 if cw < cmw else cw) for cw, cmw in zip(self._FixedColumnWidthTable__column_widths, column_max_widths)]

            # calculate number of expandable columns
            number_of_expandable_columns = sum([1 if cw < cmw else 0 for cw, cmw in zip(self._FixedColumnWidthTable__column_widths, column_max_widths)])

            # calculate remaining width
            remaining_width = available_space[0] - sum(self._FixedColumnWidthTable__column_widths)

        # fmt: on

    @staticmethod
    def __narrowest_landscape_box(e: LayoutElement) -> typing.Tuple[int, int]:
        POSITIVE_INT_INFINITY: int = 2**64
        width_upper: int = e.get_size(
            available_space=(POSITIVE_INT_INFINITY, POSITIVE_INT_INFINITY)
        )[0]
        width_lower: int = 1
        while abs(width_upper - width_lower) > 2:
            width_midpoint: int = (width_upper + width_lower) // 2
            w: int = e.get_size(
                available_space=(width_midpoint, POSITIVE_INT_INFINITY)
            )[0]
            if w >= width_midpoint:
                width_lower = width_midpoint
            if w < width_midpoint:
                width_upper = width_midpoint
        return e.get_size(available_space=(width_upper, POSITIVE_INT_INFINITY))

    @staticmethod
    def __widest_landscape_box(e: LayoutElement) -> typing.Tuple[int, int]:
        POSITIVE_INT_INFINITY: int = 2**64
        return e.get_size(
            available_space=(POSITIVE_INT_INFINITY, POSITIVE_INT_INFINITY)
        )

    #
    # PUBLIC
    #

    @functools.cache
    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        self.__calculate_and_set_column_width(available_space=available_space)
        return super().get_size(available_space=available_space)
