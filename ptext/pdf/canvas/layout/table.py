#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains everything needed to lay out tables
"""
import typing
import zlib
from decimal import Decimal

from ptext.io.read.types import Name
from ptext.pdf.canvas.color.color import X11Color, Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.layout_element import Alignment
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
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        background_color: typing.Optional[Color] = None,
    ):
        super(TableCell, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            background_color=background_color,
        )
        self.layout_element = layout_element
        assert row_span >= 1
        assert col_span >= 1
        assert not isinstance(layout_element, TableCell)
        assert not isinstance(layout_element, Table)
        self.row_span = row_span
        self.col_span = col_span

    def layout(self, page: Page, layout_box: Rectangle) -> Rectangle:
        self.layout_element.padding_top = self.padding_top
        self.layout_element.padding_right = self.padding_right
        self.layout_element.padding_bottom = self.padding_bottom
        self.layout_element.padding_left = self.padding_left
        box: Rectangle = self.layout_element.layout(page, layout_box)
        self.set_bounding_box(box)
        return box

    def _draw_border(self, page: Page, border_box: Rectangle):
        # This method is purposefully blank, to ensure the parent (Table)
        # is the only element that gets to call the _draw_border_after_layout method
        # which properly renders the borders.
        pass

    def _draw_border_after_layout(self, page: Page, border_box: Rectangle):
        super(TableCell, self)._draw_border(page, border_box)

    def _draw_background(self, page: Page, border_box: Rectangle):
        # This method is purposefully blank, to ensure the parent (Table)
        # is the only element that gets to call the _draw_background_after_layout method
        # which properly renders the background.
        pass

    def _draw_background_after_layout(self, page: Page, border_box: Rectangle):
        super(TableCell, self)._draw_background(page, border_box)


class Table(LayoutElement):
    """
    This class represents a layout table
    """

    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        column_widths: typing.List[Decimal] = [],
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
        background_color: typing.Optional[Color] = None,
    ):
        super(Table, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            background_color=background_color,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
        )
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

    def set_padding_on_all_cells(
        self,
        padding_top: Decimal,
        padding_right: Decimal,
        padding_bottom: Decimal,
        padding_left: Decimal,
    ) -> "Table":
        """
        This method sets the padding on all TableCell objects in this Table
        """
        for e in self.content:
            e.padding_top = padding_top
            e.padding_right = padding_right
            e.padding_bottom = padding_bottom
            e.padding_left = padding_left
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

    def outer_borders(self):
        """
        This method unsets the border(s) on all TableCell objects in this Table
        except for the borders that form the outside edge of the Table
        """
        self.no_borders()
        # TODO
        return self

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        content_stream = page["Contents"]
        len_decoded_bytes_before = len(content_stream[Name("DecodedBytes")])

        # layout elements in grid
        # this matrix ensures we can easily check which element is located at (x,y) even if there are
        # TableCell elements with row_span and col_span
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

        # set up datastructures for main layout loop
        already_laid_out: typing.List[LayoutElement] = []
        bottom_row_mtx = [
            [Decimal(-1) for _ in range(0, self.number_of_columns)]
            for _ in range(0, self.number_of_rows)
        ]

        # execute main layout loop
        previous_row_bottom = bounding_box.y + bounding_box.height
        row_boundaries: typing.List[Decimal] = [previous_row_bottom]
        for r in range(0, self.number_of_rows):
            for c in range(0, self.number_of_columns):
                e = self.content[mtx[r][c]]
                if e in already_laid_out:
                    continue
                rect_out = e.layout(
                    page,
                    Rectangle(
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
                    if self.content[mtx[r][i]].row_span == 1
                    and self.content[mtx[r][i]].get_bounding_box().height > 0
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
        already_drawn_border: typing.Dict[LayoutElement, Rectangle] = {}
        for r in range(0, self.number_of_rows):
            for c in range(0, self.number_of_columns):
                e = self.content[mtx[r][c]]
                if e in already_drawn_border:
                    continue

                border_box = Rectangle(
                    column_boundaries[c],
                    row_boundaries[r + e.row_span],
                    column_boundaries[c + e.col_span] - column_boundaries[c],
                    row_boundaries[r] - row_boundaries[r + e.row_span],
                )

                # Due to rounding errors, setting the bounding box is not trivial
                # This code cheats that system.
                # The first row is laid out to its integer-rounded coordinates,
                # every row after that is matched to the row above it
                if r == 0:
                    border_box.height = Decimal(int(border_box.height))
                    border_box.y = Decimal(int(border_box.y))

                if r != 0:
                    nb = self.content[mtx[r - 1][c]]
                    if nb is not None and nb in already_drawn_border:
                        up_bb = already_drawn_border[nb]
                        border_box.y = Decimal(int(border_box.y))
                        border_box.height = up_bb.y - border_box.y

                # set the bounding box of a cell to equal its border box
                e.set_bounding_box(border_box)

                # draw the border
                e._draw_border_after_layout(page, border_box)

                # mark the border as already drawn
                already_drawn_border[e] = border_box

        # change content stream to put background before rendering of the content
        added_content = content_stream[Name("DecodedBytes")][len_decoded_bytes_before:]
        content_stream[Name("DecodedBytes")] = content_stream[Name("DecodedBytes")][
            0:len_decoded_bytes_before
        ]

        # draw backgrounds
        for table_cell in self.content:
            assert table_cell.bounding_box is not None
            table_cell._draw_background_after_layout(page, table_cell.bounding_box)

        # re-add content
        content_stream[Name("DecodedBytes")] += added_content
        content_stream[Name("Bytes")] = zlib.compress(
            content_stream[Name("DecodedBytes")], 9
        )
        content_stream[Name("Length")] = len(content_stream[Name("Bytes")])

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
