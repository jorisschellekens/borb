#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a Table with columns that will assume
a width based on their contents. It tries to emulate the behaviour
of <table> elements in HTML
"""
import typing
import zlib
from decimal import Decimal
from math import floor

from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.table.table import Table, TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page


class FlexibleColumnWidthTable(Table):
    """
    This class represents a Table with columns that will assume
    a width based on their contents. It tries to emulate the behaviour
    of <table> elements in HTML
    """

    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
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
        super(FlexibleColumnWidthTable, self).__init__(
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
            margin_bottom=margin_bottom or Decimal(5),
            margin_left=margin_left or Decimal(5),
            margin_right=margin_right or Decimal(5),
            margin_top=margin_top or Decimal(5),
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )

    def _do_layout_without_padding(
        self,
        page: "Page",
        bounding_box: Rectangle,  # type: ignore[name-defined]
        do_layout: bool = False,
    ) -> Rectangle:
        # 1.    Calculate the minimum content width (MCW) of each cell: the formatted content may span any number of lines but may not overflow the cell box.
        #       If the specified 'width' (W) of the cell is greater than MCW, W is the minimum cell width.
        #       A value of 'auto' means that MCW is the minimum cell width.
        #
        #       Also, calculate the "maximum" cell width of each cell:
        #       formatting the content without breaking lines other than where explicit line breaks occur.
        for t in self._content:
            t.calculate_min_and_max_width()

        # 2.    For each column, determine a maximum and minimum column width from the cells that span only that column.
        #       The minimum is that required by the cell with the largest minimum cell width (or the column 'width', whichever is larger).
        #       The maximum is that required by the cell with the largest maximum cell width (or the column 'width', whichever is larger).
        min_column_widths: typing.List[Decimal] = []
        max_column_widths: typing.List[Decimal] = []
        for i in range(0, self._number_of_columns):
            column_content: typing.List[TableCell] = [
                x for x in self._get_cells_at_column(i) if x._col_span == 1
            ]
            if len(column_content) == 0:
                min_column_widths.append(Decimal(0))
                max_column_widths.append(Decimal(2048))
            else:
                # DIFFERENCE WITH CSS : if the column has a preferred width AND the preferred width is larger than or equal to the min width,
                # the column is assigned its preferred width
                min_column_widths.append(
                    max(
                        [
                            (
                                x._preferred_width
                                if x._preferred_width is not None
                                and x._min_width is not None
                                and x._preferred_width >= x._min_width
                                else x._min_width
                            )
                            or Decimal(0)
                            for x in column_content
                        ]
                    )
                    + Decimal(1)
                )
                # DIFFERENCE WITH CSS : if the column has a preferred width AND the preferred width is less than or equal to the max width,
                # the column is assigned its preferred width
                max_column_widths.append(
                    max(
                        [
                            (
                                x._preferred_width
                                if x._preferred_width is not None
                                and x._max_width is not None
                                and x._preferred_width <= x._max_width
                                else x._max_width
                            )
                            or Decimal(0)
                            for x in column_content
                        ]
                    )
                    + Decimal(1)
                )

        # 3.    For each cell that spans more than one column, increase the minimum widths of the columns it spans so that together,
        #       they are at least as wide as the cell. Do the same for the maximum widths.
        #       If possible, widen all spanned columns by approximately the same amount.
        for t in [x for x in self._content if x._col_span != 1]:

            cols_in_span: typing.List[int] = [
                y for y in set([x[1] for x in t._table_coordinates])
            ]
            total_col_span_min_width = sum([min_column_widths[x] for x in cols_in_span])
            assert t._min_width is not None
            if total_col_span_min_width < t._min_width:
                col_span_min_width_delta: Decimal = (
                    t._min_width - total_col_span_min_width
                )
                for c in cols_in_span:
                    min_column_widths[c] += col_span_min_width_delta / Decimal(
                        len(cols_in_span)
                    )

            total_col_span_max_width = sum([min_column_widths[x] for x in cols_in_span])
            assert t._max_width is not None
            if total_col_span_max_width < t._max_width:
                col_span_max_width_delta: Decimal = (
                    t._max_width - total_col_span_max_width
                )
                for c in cols_in_span:
                    max_column_widths[c] += col_span_max_width_delta / Decimal(
                        len(cols_in_span)
                    )

        # 4.    For each column group element with a 'width' other than 'auto', increase the minimum widths of the columns it spans,
        #       so that together they are at least as wide as the column group's 'width'.
        #
        # This gives a maximum and minimum width for each column.

        # 5. calculate column width based on min, max and bounding box
        # start by assigning each column its minimum width
        column_widths: typing.List[Decimal] = [x for x in min_column_widths]

        # as long as there are columns that could be expanded, and there is room to expand them
        # add Decimal(1) to each (expandable) column_width
        number_of_expandable_columns: int = sum(
            [
                1
                for i in range(0, len(column_widths))
                if column_widths[i] < max_column_widths[i]
            ]
        )
        while (
            sum(column_widths) + number_of_expandable_columns < bounding_box.get_width()
            and number_of_expandable_columns > 0
        ):
            for i in range(0, len(column_widths)):
                if column_widths[i] < max_column_widths[i]:
                    column_widths[i] += Decimal(1)
            number_of_expandable_columns = sum(
                [
                    1
                    for i in range(0, len(column_widths))
                    if column_widths[i] < max_column_widths[i]
                ]
            )

        # auto fill table
        empty_cells: int = self._number_of_rows * self._number_of_columns - sum(
            [(x._row_span * x._col_span) for x in self._content]
        )
        for _ in range(0, empty_cells):
            self.add(Paragraph(" ", respect_spaces_in_text=True))

        # calculate column bounds
        column_bounds: typing.List[Decimal] = [bounding_box.get_x()]
        for cw in column_widths:
            column_bounds.append(column_bounds[-1] + cw)

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
            assert len(t._table_coordinates) > 0
            x: Decimal = column_bounds[min([p[1] for p in t._table_coordinates])]
            w: Decimal = (
                column_bounds[max([p[1] for p in t._table_coordinates]) + 1] - x
            )
            y: Decimal = Decimal(0)
            h: Decimal = row_bounds[min([p[0] for p in t._table_coordinates])]

            # layout
            t.layout(page, Rectangle(x, y, w, h))
            tbb: typing.Optional[Rectangle] = t.get_bounding_box()
            assert tbb is not None

            # update row_bounds
            preferred_y: Decimal = (
                (tbb.get_y() + tbb.get_height() - t._preferred_height)
                if t._preferred_height is not None
                and t._preferred_height >= tbb.get_height()
                else tbb.get_y()
            )
            max_row = max([p[0] for p in t._table_coordinates]) + 1
            row_bounds[max_row] = min(row_bounds[max_row], Decimal(floor(preferred_y)))

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

        # draw backgrounds
        for t in self._content:
            assert t.bounding_box is not None
            t._draw_background_after_layout(page, t.bounding_box)

        # draw borders
        for t in self._content:
            assert t.bounding_box is not None
            t._draw_border_after_layout(page)

        # re-add content
        page["Contents"][Name("DecodedBytes")] += table_content_bytes
        page["Contents"][Name("Bytes")] = zlib.compress(
            page["Contents"][Name("DecodedBytes")], 9
        )
        page["Contents"][Name("Length")] = len(page["Contents"][Name("Bytes")])

        # return
        return bounding_box
