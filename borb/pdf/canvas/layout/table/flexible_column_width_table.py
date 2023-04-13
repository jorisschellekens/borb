#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a Table with columns that will assume
a width based on their contents. It tries to emulate the behaviour
of <table> elements in HTML
"""
import math
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page


class FlexibleColumnWidthTable(Table):
    """
    This class represents a Table with columns that will assume
    a width based on their contents. It tries to emulate the behaviour
    of <table> elements in HTML
    """

    #
    # CONSTRUCTOR
    #

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
            margin_bottom=margin_bottom if margin_bottom is not None else Decimal(5),
            margin_left=margin_left if margin_left is not None else Decimal(5),
            margin_right=margin_right if margin_right is not None else Decimal(5),
            margin_top=margin_top if margin_top is not None else Decimal(5),
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:

        # fill table
        number_of_cells: int = self._number_of_rows * self._number_of_columns
        empty_cells: int = number_of_cells - sum(
            [(x._row_span * x._col_span) for x in self._content]
        )
        for _ in range(0, empty_cells):
            self.add(Paragraph(" ", respect_spaces_in_text=True))

        # return
        m = self._get_grid_coordinates(available_space)
        min_x: Decimal = m[0][0][0]
        max_x: Decimal = m[-1][-1][0]
        min_y: Decimal = m[-1][-1][1]
        max_y: Decimal = m[0][0][1]
        return Rectangle(
            available_space.get_x(),
            min_y,
            Decimal(math.ceil(max_x - min_x)),
            max_y - min_y,
        )

    def _get_grid_coordinates(
        self,
        available_space: Rectangle,  # type: ignore[name-defined]
    ) -> typing.List[typing.List[typing.Tuple[Decimal, Decimal]]]:
        # 1.    Calculate the minimum content width (MCW) of each cell: the formatted content may span any number of lines but may not overflow the cell box.
        #       If the specified 'width' (W) of the cell is greater than MCW, W is the minimum cell width.
        #       A value of 'auto' means that MCW is the minimum cell width.
        #
        #       Also, calculate the "maximum" cell width of each cell:
        #       formatting the content without breaking lines other than where explicit line breaks occur.
        for t in self._content:
            t._calculate_min_and_max_layout_box()

        # 2.    For each column, determine a maximum and minimum column width from the cells that span only that column.
        #       The minimum is that required by the cell with the largest minimum cell width (or the column 'width', whichever is larger).
        #       The maximum is that required by the cell with the largest maximum cell width (or the column 'width', whichever is larger).
        min_column_widths: typing.List[Decimal] = [
            self._get_min_column_width(i) for i in range(0, self._number_of_columns)
        ]
        max_column_widths: typing.List[Decimal] = [
            self._get_max_column_width(i) for i in range(0, self._number_of_columns)
        ]

        # 3.    For each cell that spans more than one column, increase the minimum widths of the columns it spans so that together,
        #       they are at least as wide as the cell. Do the same for the maximum widths.
        #       If possible, widen all spanned columns by approximately the same amount.
        for table_cell in self._content:
            if table_cell._col_span == 1:
                continue
            column_indices: typing.Set[int] = set(
                [y for x, y in table_cell._table_coordinates]
            )
            sum_of_min_col_spans: Decimal = Decimal(
                sum([min_column_widths[x] for x in column_indices])
            )
            assert table_cell._min_width is not None
            if sum_of_min_col_spans < table_cell._min_width:
                delta: Decimal = table_cell._min_width - sum_of_min_col_spans
                min_column_widths = [
                    w + (delta / table_cell._col_span) if i in column_indices else w
                    for i, w in enumerate(min_column_widths)
                ]

            sum_of_max_col_spans: Decimal = Decimal(
                sum([max_column_widths[x] for x in column_indices])
            )
            assert table_cell._max_width is not None
            if sum_of_max_col_spans < table_cell._max_width:
                delta = table_cell._max_width - sum_of_max_col_spans
                max_column_widths = [
                    w + (delta / table_cell._col_span) if i in column_indices else w
                    for i, w in enumerate(max_column_widths)
                ]

        # 4.    For each column group element with a 'width' other than 'auto', increase the minimum widths of the columns it spans,
        #       so that together they are at least as wide as the column group's 'width'.
        #       This gives a maximum and minimum width for each column.

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
            sum(column_widths) + number_of_expandable_columns
            < available_space.get_width()
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

        # convert grid coordinates to page coordinates
        grid_x_to_page_x: typing.List[Decimal] = [available_space.get_x()]
        for i in range(1, self._number_of_columns + 1):
            prev_x: Decimal = grid_x_to_page_x[-1]
            new_x: Decimal = prev_x + column_widths[i - 1]
            grid_x_to_page_x.append(new_x)

        # calculate bounds of TableCells with row_span == 1
        grid_y_to_page_y: typing.List[Decimal] = [
            available_space.get_y() + available_space.get_height()
        ]
        for r in range(0, self._number_of_rows):
            prev_row_lboxes: typing.List[Rectangle] = []
            for e in [x for x in self._get_cells_at_row(r) if x._row_span == 1]:

                # get coordinates of lower-left corner of this TableCell (in grid space)
                # table keeps track of things in (row, column) style
                # hence p[1], rather than p[0]
                grid_x: int = min([p[1] for p in e._table_coordinates])

                # layout
                prev_vertical_alignment = e._layout_element._vertical_alignment
                e._layout_element._vertical_alignment = Alignment.TOP
                prev_row_lboxes.append(
                    e.get_layout_box(
                        Rectangle(
                            grid_x_to_page_x[grid_x],
                            available_space.get_y(),
                            grid_x_to_page_x[grid_x + e._col_span]
                            - grid_x_to_page_x[grid_x],
                            max(
                                grid_y_to_page_y[r] - available_space.get_y(),
                                Decimal(0),
                            ),
                        )
                    )
                )
                e._layout_element._vertical_alignment = prev_vertical_alignment

            # keep track of the bottom of the previous (at this point current) row
            # this makes it easier to lay out the next row
            new_y: Decimal = min([lbox.get_y() for lbox in prev_row_lboxes])
            row_height: Decimal = grid_y_to_page_y[-1] - new_y
            grid_y_to_page_y.append(new_y)

            # do a second pass, this time with the right vertical alignment
            # now that we know the tallest element (and thus the row height)
            for e in [x for x in self._get_cells_at_row(r) if x._row_span == 1]:
                grid_x: int = min([p[1] for p in e._table_coordinates])
                if e._layout_element._vertical_alignment == Alignment.TOP:
                    continue
                e.get_layout_box(
                    Rectangle(
                        grid_x_to_page_x[grid_x],
                        new_y,
                        grid_x_to_page_x[grid_x + e._col_span]
                        - grid_x_to_page_x[grid_x],
                        row_height,
                    )
                )

        # return
        return [[(x, y) for y in grid_y_to_page_y] for x in grid_x_to_page_x]

    def _get_max_column_width(self, col: int) -> Decimal:
        widths: typing.List[Decimal] = []
        for table_cell in [
            x for x in self._get_cells_at_column(col) if x._col_span == 1
        ]:
            if table_cell._max_width is None:
                widths.append(Decimal(2048))
                continue
            if table_cell._preferred_width is None:
                widths.append(table_cell._max_width)
                continue
            if table_cell._preferred_width < table_cell._max_width:
                widths.append(table_cell._preferred_width)
                continue
            # default
            widths.append(table_cell._max_width)

        # exception
        if len(widths) == 0:
            return Decimal(2048)

        # return
        return max(widths)

    def _get_min_column_width(self, col: int) -> Decimal:
        widths: typing.List[Decimal] = []
        for table_cell in [
            x for x in self._get_cells_at_column(col) if x._col_span == 1
        ]:
            if table_cell._min_width is None:
                widths.append(Decimal(0))
                continue
            if table_cell._preferred_width is None:
                assert table_cell._min_width is not None
                widths.append(table_cell._min_width)
                continue
            if table_cell._preferred_width > table_cell._min_width:
                assert table_cell._preferred_width is not None
                widths.append(table_cell._preferred_width)
                continue
            # default
            assert table_cell._min_width is not None
            widths.append(table_cell._min_width)

        # exception
        if len(widths) == 0:
            return Decimal(0)

        # return
        return max(widths)

    def _paint_content_box(self, page: Page, available_space: Rectangle) -> None:

        # fill table
        number_of_cells: int = self._number_of_rows * self._number_of_columns
        empty_cells: int = number_of_cells - sum(
            [(x._row_span * x._col_span) for x in self._content]
        )
        for _ in range(0, empty_cells):
            self.add(Paragraph(" ", respect_spaces_in_text=True))

        m: typing.List[
            typing.List[typing.Tuple[Decimal, Decimal]]
        ] = self._get_grid_coordinates(available_space)

        # paint
        for e in self._content:
            grid_x: int = min([p[1] for p in e._table_coordinates])
            grid_y: int = min([p[0] for p in e._table_coordinates])
            x: Decimal = m[grid_x][grid_y][0]
            y: Decimal = m[grid_x][grid_y + e._row_span][1]
            w: Decimal = m[grid_x + e._col_span][grid_y][0] - x
            h: Decimal = m[grid_x][grid_y][1] - y
            cbox: Rectangle = Rectangle(x, y, w, h)
            e._set_layout_box(cbox)
            e.paint(page, cbox)

    #
    # PUBLIC
    #
