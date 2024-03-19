#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a Table with columns of fixed width
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page


class FixedColumnWidthTable(Table):
    """
    This class represents a Table with columns of fixed width
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        column_widths: typing.List[Decimal] = [],
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: Decimal = Decimal(0),
        margin_left: Decimal = Decimal(0),
        margin_right: Decimal = Decimal(0),
        margin_top: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(FixedColumnWidthTable, self).__init__(
            number_of_rows=number_of_rows,
            number_of_columns=number_of_columns,
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
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
        if len(column_widths) == 0:
            column_widths = [Decimal(1) for _ in range(0, number_of_columns)]
        assert len(column_widths) == number_of_columns
        self._column_widths: typing.List[Decimal] = column_widths

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        # fill table
        number_of_cells: int = self._number_of_rows * self._number_of_columns
        empty_cells: int = number_of_cells - sum(
            [(x.get_row_span() * x.get_column_span()) for x in self._content]
        )
        for _ in range(0, empty_cells):
            self.add(Paragraph(" ", respect_spaces_in_text=True))

        # return
        min_y: Decimal = self._get_grid_coordinates(available_space)[-1][-1][1]
        return Rectangle(
            available_space.get_x(),
            min_y,
            available_space.get_width(),
            available_space.get_y() + available_space.get_height() - min_y,
        )

    def _get_grid_coordinates(
        self, available_space: Rectangle
    ) -> typing.List[typing.List[typing.Tuple[Decimal, Decimal]]]:
        # normalize column widths
        self._column_widths = [
            x / sum(self._column_widths) for x in self._column_widths
        ]

        # convert grid coordinates to page coordinates
        grid_x_to_page_x: typing.List[Decimal] = [available_space.get_x()]
        for i in range(1, self._number_of_columns + 1):
            prev_x: Decimal = grid_x_to_page_x[-1]
            new_x: Decimal = (
                prev_x + available_space.get_width() * self._column_widths[i - 1]
            )
            grid_x_to_page_x.append(new_x)

        # calculate bounds of TableCells with row_span == 1
        grid_y_to_page_y: typing.List[Decimal] = [
            available_space.get_y() + available_space.get_height()
        ]
        for r in range(0, self._number_of_rows):
            prev_row_lboxes: typing.List[Rectangle] = []

            # we do a first pass over each row to determine how tall the row needs to be
            # we temporarily change every LayoutElement's vertical alignment
            # then we reset it to its previous value
            for e in [x for x in self.get_cells_at_row(r) if x.get_row_span() == 1]:
                # get coordinates of lower-left corner of this TableCell (in grid space)
                # table keeps track of things in (row, column) style
                # hence p[1], rather than p[0]
                grid_x: int = min([p[1] for p in e.get_table_coordinates()])

                # layout
                prev_vertical_alignment = e.get_layout_element()._vertical_alignment
                e.get_layout_element()._vertical_alignment = Alignment.TOP
                prev_row_lboxes.append(
                    e.get_layout_box(
                        Rectangle(
                            grid_x_to_page_x[grid_x],
                            available_space.get_y(),
                            grid_x_to_page_x[grid_x + e.get_column_span()]
                            - grid_x_to_page_x[grid_x],
                            max(
                                Decimal(0),
                                grid_y_to_page_y[r] - available_space.get_y(),
                            ),
                        )
                    )
                )
                e.get_layout_element()._vertical_alignment = prev_vertical_alignment

            # keep track of the bottom of the previous (at this point current) row
            # this makes it easier to lay out the next row
            new_y: Decimal = min([lbox.get_y() for lbox in prev_row_lboxes])
            row_height: Decimal = grid_y_to_page_y[-1] - new_y
            grid_y_to_page_y.append(new_y)

            # do a second pass, this time with the right vertical alignment
            # now that we know the tallest element (and thus the row height)
            for e in [x for x in self.get_cells_at_row(r) if x.get_row_span() == 1]:
                grid_x = min([p[1] for p in e.get_table_coordinates()])
                if e.get_layout_element()._vertical_alignment == Alignment.TOP:
                    continue
                e.get_layout_box(
                    Rectangle(
                        grid_x_to_page_x[grid_x],
                        new_y,
                        grid_x_to_page_x[grid_x + e.get_column_span()]
                        - grid_x_to_page_x[grid_x],
                        row_height,
                    )
                )

        # layout TableCells that span more than 1 row
        # TODO

        # return
        return [[(x, y) for y in grid_y_to_page_y] for x in grid_x_to_page_x]

    def _paint_content_box(self, page: Page, available_space: Rectangle) -> None:
        # fill table
        number_of_cells: int = self._number_of_rows * self._number_of_columns
        empty_cells: int = number_of_cells - sum(
            [(x.get_row_span() * x.get_column_span()) for x in self._content]
        )
        for _ in range(0, empty_cells):
            self.add(Paragraph(" ", respect_spaces_in_text=True))

        m: typing.List[
            typing.List[typing.Tuple[Decimal, Decimal]]
        ] = self._get_grid_coordinates(available_space)

        # paint
        for e in self._content:
            grid_x: int = min([p[1] for p in e.get_table_coordinates()])
            grid_y: int = min([p[0] for p in e.get_table_coordinates()])
            cbox: Rectangle = Rectangle(
                m[grid_x][grid_y][0],
                m[grid_x][grid_y + e.get_row_span()][1],
                m[grid_x + e.get_column_span()][grid_y][0] - m[grid_x][grid_y][0],
                m[grid_x][grid_y][1] - m[grid_x][grid_y + e.get_row_span()][1],
            )
            e._set_layout_box(cbox)
            e.paint(page, cbox)

    #
    # PUBLIC
    #
