#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a table with fixed column widths.

The `FixedColumnWidthTable` class is used to create a table layout where each column
has a predefined and fixed width, regardless of the content. This ensures consistent
alignment and appearance across all rows, making it suitable for structured data where
uniformity in column width is important.
"""
import functools
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.table.table import Table
from borb.pdf.page import Page

GridPointType: typing.TypeAlias = typing.Tuple[int, int]


class FixedColumnWidthTable(Table):
    """
    Represents a table with fixed column widths.

    The `FixedColumnWidthTable` class is used to create a table layout where each column
    has a predefined and fixed width, regardless of the content. This ensures consistent
    alignment and appearance across all rows, making it suitable for structured data where
    uniformity in column width is important.
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
        column_widths: typing.Optional[typing.List[int]] = None,
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
        :param column_widths:           Optional list specifying the width of each column.
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
        self.__column_widths: typing.List[int] = column_widths or [
            1 for _ in range(0, number_of_columns)
        ]

    #
    # PRIVATE
    #

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
        # calculate column_widths
        # IF we are a FlexibleColumnWidthTable
        # THEN avoid "normalizing" the widths (aka interpreting them as a ratio of the FULL page width)
        # fmt: off
        from borb.pdf.layout_element.table.flexible_column_width_table import \
            FlexibleColumnWidthTable
        if not isinstance(self, FlexibleColumnWidthTable):
            w_avail: int = available_space[0] - self.get_padding_left() - self.get_padding_right()
            self.__column_widths = [int((x / sum(self.__column_widths)) * w_avail) for x in self.__column_widths]
            self.__column_widths[0] += (w_avail - sum(self.__column_widths))
        # fmt: on

        # utility function to get the column_width for a given element
        def _get_available_width(e: Table.TableCell) -> int:
            # fmt: off
            cs: typing.Set[int] = set([c for _, c in self._Table__inner_layout_element_to_table_coordinates[e]])    # type: ignore[attr-defined]
            return sum([self.__column_widths[c] for c in cs])
            # fmt: on

        # loop over each row, determining the min_row_height
        row_height: typing.List[int] = [0 for _ in range(self._Table__number_of_rows)]  # type: ignore[attr-defined]
        for row_index in range(0, self._Table__number_of_rows):  # type: ignore[attr-defined]
            row_height[row_index] = max(
                [
                    math.ceil(
                        e.get_size(available_space=(_get_available_width(e), 2**64))[1]
                        / e.get_row_span()
                    )
                    for e in self.get_row(row_index)
                ]
            )

        # return
        return (
            sum(self.__column_widths)
            + self.get_padding_left()
            + self.get_padding_right(),
            sum(row_height) + self.get_padding_top() + self.get_padding_bottom(),
        )

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        # determine width/height
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))

        # calculate where the background/borders need to be painted
        # fmt: off
        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.LEFT:
            background_x = available_space[0]
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)
        # fmt: on

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # paint background and border(s)
        self._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # calculate column_widths
        # fmt: off
        w_avail: int = w - self.get_padding_left() - self.get_padding_right()
        column_widths: typing.List[int] = [int((x / sum(self.__column_widths)) * w_avail) for x in self.__column_widths]
        column_widths[0] += (w_avail - sum(column_widths))
        # fmt: on

        # grid_x to pts_x
        # fmt: off
        grid_x_to_pts_x: typing.Dict[int, int] = {0: background_x + self.get_padding_left()}
        for i in range(0, self._Table__number_of_columns):                                      # type: ignore[attr-defined]
            grid_x_to_pts_x[i + 1] = grid_x_to_pts_x[i] + column_widths[i]
        # fmt: on

        # utility function to get the column_width for a given element
        def _get_available_width(e: Table.TableCell) -> int:
            # fmt: off
            cs: typing.Set[int] = set([c for _, c in self._Table__inner_layout_element_to_table_coordinates[e]])    # type: ignore[attr-defined]
            return sum([column_widths[c] for c in cs])
            # fmt: on

        # loop over each row, determining the min_row_height
        row_heights: typing.List[int] = [0 for _ in range(self._Table__number_of_rows)]  # type: ignore[attr-defined]
        for row_index in range(0, self._Table__number_of_rows):  # type: ignore[attr-defined]
            row_heights[row_index] = max(
                [
                    math.ceil(
                        e.get_size(available_space=(_get_available_width(e), 2**64))[1]
                        / e.get_row_span()
                    )
                    for e in self.get_row(row_index)
                ]
            )

        # convert grid_y to pts_y
        # fmt: off
        top_y: int = background_y + h - self.get_padding_top()
        grid_y_to_pts_y: typing.Dict[int, int] = {0: top_y}
        for i in range(0, len(row_heights)):
            grid_y_to_pts_y[i + 1] = grid_y_to_pts_y[i] - row_heights[i]
        # fmt: on

        # lay out each TableCell individually
        for e in self._Table__inner_layout_elements:  # type: ignore[attr-defined]

            # calculate coordinates for layout (in grid)
            # fmt: off
            min_grid_row: int = min([r for r, _ in self._Table__inner_layout_element_to_table_coordinates[e]])  # type: ignore[attr-defined]
            min_grid_col: int = min([c for _, c in self._Table__inner_layout_element_to_table_coordinates[e]])  # type: ignore[attr-defined]
            max_grid_row: int = max([r for r, _ in self._Table__inner_layout_element_to_table_coordinates[e]])  # type: ignore[attr-defined]
            max_grid_col: int = max([c for _, c in self._Table__inner_layout_element_to_table_coordinates[e]])  # type: ignore[attr-defined]
            # fmt: on

            # convert to pts
            min_y: int = grid_y_to_pts_y[min_grid_row]
            max_y: int = grid_y_to_pts_y[max_grid_row + 1]
            min_x: int = grid_x_to_pts_x[min_grid_col]
            max_x: int = grid_x_to_pts_x[max_grid_col + 1]

            e.paint(
                available_space=(min_x, max_y, max_x - min_x, abs(max_y - min_y)),
                page=page,
            )
