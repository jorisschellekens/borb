#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a Table with columns of fixed width
"""
import typing
import zlib
from decimal import Decimal
from math import floor

from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color, HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page


class FixedColumnWidthTable(Table):
    """
    This class represents a Table with columns of fixed width
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
        border_color: Color = HexColor("000000"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        margin_top: Decimal = Decimal(0),
        margin_right: Decimal = Decimal(0),
        margin_bottom: Decimal = Decimal(0),
        margin_left: Decimal = Decimal(0),
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
        background_color: typing.Optional[Color] = None,
    ):
        super(FixedColumnWidthTable, self).__init__(
            number_of_rows=number_of_rows,
            number_of_columns=number_of_columns,
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
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            background_color=background_color,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
        )
        if len(column_widths) == 0:
            column_widths = [Decimal(1) for _ in range(0, number_of_columns)]
        assert len(column_widths) == number_of_columns
        self._column_widths: typing.List[Decimal] = column_widths

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # calculate column_bounds
        column_bounds: typing.List[Decimal] = [bounding_box.get_x()]
        total_column_width: Decimal = Decimal(sum(self._column_widths))
        for i in range(0, len(self._column_widths)):
            column_bounds.append(
                column_bounds[-1]
                + (
                    bounding_box.get_width()
                    * self._column_widths[i]
                    / total_column_width
                )
            )

        # auto fill table
        number_of_cells: int = self._number_of_rows * self._number_of_columns
        empty_cells: int = number_of_cells - sum(
            [(x._row_span * x._col_span) for x in self._content]
        )
        for _ in range(0, empty_cells):
            self.add(Paragraph(" ", respect_spaces_in_text=True))

        # We are going to store the offset, to ensure we can draw backgrounds and borders later.
        # We want backgrounds and borders to be drawn first, which requires us to mess around
        # with the raw content bytes a bit.
        # This is not exactly an ideal solution, but it is a fast solution.
        page_content_stream_marker = len(page["Contents"][Name("DecodedBytes")])

        # lay out content
        row_bounds: typing.List[Decimal] = [
            Decimal(floor(bounding_box.get_y() + bounding_box.get_height()))
            for _ in range(0, self._number_of_rows + 1)
        ]
        for t in self._content:

            # calculate bounds
            # fmt: off
            assert len(t._table_coordinates) > 0
            x: Decimal = column_bounds[min([p[1] for p in t._table_coordinates])]
            w: Decimal = column_bounds[max([p[1] for p in t._table_coordinates]) + 1] - x
            y: Decimal = Decimal(0)
            h: Decimal = row_bounds[min([p[0] for p in t._table_coordinates])]
            # fmt: on

            # layout
            t.layout(page, Rectangle(x, y, w, h))
            tbb: typing.Optional[Rectangle] = t.get_bounding_box()
            assert tbb is not None

            # update row_bounds
            max_row = max([p[0] for p in t._table_coordinates]) + 1
            row_bounds[max_row] = min(row_bounds[max_row], Decimal(floor(tbb.get_y())))

        # update bounds of content
        for t in self._content:
            x = column_bounds[min([p[1] for p in t._table_coordinates])]
            w = column_bounds[max([p[1] for p in t._table_coordinates]) + 1] - x
            max_row = max([p[0] for p in t._table_coordinates]) + 1
            min_row = min([p[0] for p in t._table_coordinates])
            y = row_bounds[max_row]
            h = row_bounds[min_row] - y
            t.bounding_box = Rectangle(x, y, w, h)

        # calculate bounding box
        # fmt: off
        bounding_box = Rectangle(
            min([x.get_bounding_box().get_x() for x in self._content]),     # type: ignore [union-attr]
            min([x.get_bounding_box().get_y() for x in self._content]),     # type: ignore [union-attr]
            max([x.get_bounding_box().get_x() + x.get_bounding_box().get_width() for x in self._content]) - min([x.get_bounding_box().get_x() for x in self._content]),     # type: ignore [union-attr]
            max([x.get_bounding_box().get_y() + x.get_bounding_box().get_height() for x in self._content]) - min([x.get_bounding_box().get_y() for x in self._content]),    # type: ignore [union-attr]
        )
        # fmt: on

        # change content stream to put background before rendering of the content
        table_content_bytes = page["Contents"][Name("DecodedBytes")][
            page_content_stream_marker:
        ]
        page["Contents"][Name("DecodedBytes")] = page["Contents"][Name("DecodedBytes")][
            0:page_content_stream_marker
        ]

        # draw borders
        for t in self._content:
            assert t.bounding_box is not None
            t._draw_border_after_layout(page)

        # draw backgrounds
        for t in self._content:
            assert t.bounding_box is not None
            t._draw_background_after_layout(page, t.bounding_box)

        # re-add content
        page["Contents"][Name("DecodedBytes")] += table_content_bytes
        page["Contents"][Name("Bytes")] = zlib.compress(
            page["Contents"][Name("DecodedBytes")], 9
        )
        page["Contents"][Name("Length")] = len(page["Contents"][Name("Bytes")])

        # return
        return bounding_box
