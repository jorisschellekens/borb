#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains everything needed to lay out tables
"""
import typing
from decimal import Decimal

from ptext.pdf.canvas.color.color import X11Color, Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import LayoutElement
from ptext.pdf.page.page import Page


class TableCell(LayoutElement):
    """
    This class represents a single cell of a table
    """

    def __init__(
        self,
        layout_element: LayoutElement,
        row_span: int = 1,
        col_span: int = 1,
        border_top: bool = True,
        border_right: bool = True,
        border_bottom: bool = True,
        border_left: bool = True,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
    ):
        super(TableCell, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
        )
        self.layout_element = layout_element
        assert row_span >= 1
        assert col_span >= 1
        assert not isinstance(layout_element, TableCell)
        assert not isinstance(layout_element, Table)
        self.row_span = row_span
        self.col_span = col_span

    def layout(self, page: Page, bounding_box: Rectangle) -> Rectangle:
        return self.layout_element.layout(page, bounding_box)


class Table(LayoutElement):
    """
    This class represents a layout table
    """

    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        column_widths: typing.List[Decimal] = [],
    ):
        assert number_of_rows >= 1
        assert number_of_columns >= 1
        if len(column_widths) == 0:
            column_widths = [Decimal(1) for _ in range(0, number_of_columns)]
        assert len(column_widths) == number_of_columns
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.column_widths = column_widths
        self.content: typing.List[TableCell] = []

    def add(self, layout_element: LayoutElement) -> "Table":
        """
        Adds a LayoutElement to this Table
        """
        if not isinstance(layout_element, TableCell):
            new_layout_element = TableCell(layout_element)
            self.content.append(new_layout_element)
        else:
            self.content.append(layout_element)
        return self

    def set_border_width_on_all_cells(self, border_width: Decimal) -> "Table":
        """
        This method sets the border width on all TableCell objects in this Table
        """
        assert border_width >= 0
        for e in self.content:
            e.border_width = border_width
        return self

    def set_border_color_on_all_cells(self, border_color: Color) -> "Table":
        """
        This method sets the border color on all TableCell objects in this Table
        """
        for e in self.content:
            e.border_color = border_color
        return self

    def set_borders_on_all_cells(
        self,
        border_top: bool,
        border_right: bool,
        border_bottom: bool,
        border_left: bool,
    ) -> "Table":
        """
        This method sets the border(s) on all TableCell objects in this Table
        """
        for e in self.content:
            e.border_top = border_top
            e.border_right = border_right
            e.border_bottom = border_bottom
            e.border_left = border_left
        return self

    def no_borders(self) -> "Table":
        """
        This method unsets the border(s) on all TableCell objects in this Table
        """
        self.set_borders_on_all_cells(False, False, False, False)
        return self

    def layout(self, page: Page, bounding_box: Rectangle):
        # layout elements in grid
        mtx = [
            [-1 for _ in range(0, self.number_of_columns)]
            for _ in range(0, self.number_of_rows)
        ]
        c = 0
        r = 0
        for i, e in enumerate(self.content):
            while mtx[r][c] != -1:
                c += 1
                if c == len(mtx[r]):
                    c = 0
                    r += 1
            for j in range(0, e.row_span):
                for k in range(0, e.col_span):
                    mtx[r + j][c + k] = i

        # calculate column edges
        column_boundaries = [
            (x / sum(self.column_widths)) * bounding_box.width
            for x in self.column_widths
        ]
        column_boundaries.insert(0, bounding_box.x)
        for i in range(1, len(column_boundaries)):
            column_boundaries[i] += column_boundaries[i - 1]

        # main layout loop
        already_laid_out: typing.List[LayoutElement] = []
        bottom_row_mtx = [
            [Decimal(-1) for _ in range(0, self.number_of_columns)]
            for _ in range(0, self.number_of_rows)
        ]

        previous_row_bottom = bounding_box.y + bounding_box.height
        row_boundaries: typing.List[Decimal] = [previous_row_bottom]
        for r in range(0, self.number_of_rows):
            for c in range(0, self.number_of_columns):
                e = self.content[mtx[r][c]]
                if e in already_laid_out:
                    continue
                rect_out = e.layout(
                    page,
                    bounding_box=Rectangle(
                        column_boundaries[c],
                        Decimal(0),
                        column_boundaries[c + e.col_span] - column_boundaries[c],
                        previous_row_bottom,
                    ),
                )

                # mark element as laid out
                already_laid_out.append(e)

                # keep track of bottom row
                for i in range(0, e.row_span):
                    for j in range(0, e.col_span):
                        bottom_row_mtx[r + i][c + j] = rect_out.y

            # recalculate previous bottom row
            previous_row_bottom = min(
                [
                    v
                    for i, v in enumerate(bottom_row_mtx[r])
                    if r == 0 or self.content[mtx[r][i]].row_span == 1
                ]
            )
            row_boundaries.append(previous_row_bottom)

        layout_rect = Rectangle(
            bounding_box.x,
            previous_row_bottom,
            bounding_box.width,
            bounding_box.y + bounding_box.height - previous_row_bottom,
        )

        # draw borders
        already_drawn_border: typing.List[LayoutElement] = []
        for r in range(0, self.number_of_rows):
            for c in range(0, self.number_of_columns):
                e = self.content[mtx[r][c]]
                if e in already_drawn_border:
                    continue
                e.draw_border(
                    page,
                    Rectangle(
                        column_boundaries[c],
                        row_boundaries[r + e.row_span],
                        column_boundaries[c + e.col_span] - column_boundaries[c],
                        row_boundaries[r] - row_boundaries[r + e.row_span],
                    ),
                )
                already_drawn_border.append(e)

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
