#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a common base for all LayoutElement implementations
that attempt to represent tabular data.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class TableCell(LayoutElement):
    """
    This class represents a single cell of a table
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        layout_element: LayoutElement,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = True,
        border_color: Color = HexColor("000000"),
        border_left: bool = True,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = True,
        border_top: bool = True,
        border_width: Decimal = Decimal(1),
        column_span: int = 1,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        preferred_height: typing.Optional[Decimal] = None,
        preferred_width: typing.Optional[Decimal] = None,
        row_span: int = 1,
    ):
        super(TableCell, self).__init__(
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
            font="Helvetica",  # not used
            font_color=HexColor("#000000"),  # not used
            font_size=Decimal(12),  # not used
            horizontal_alignment=Alignment.JUSTIFIED,  # not used
            margin_bottom=Decimal(0),  # not used
            margin_left=Decimal(0),  # not used
            margin_right=Decimal(0),  # not used
            margin_top=Decimal(0),  # not used
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=Alignment.TOP,  # not used
        )
        # fmt: off
        self._layout_element = layout_element
        assert row_span >= 1
        assert column_span >= 1
        # fmt: on

        # grid coordinates taken up by the TableCell
        self._row_span = row_span
        self._column_span = column_span
        self._table_coordinates: typing.List[typing.Tuple[int, int]] = []

        # width of the TableCell
        self._min_width: typing.Optional[Decimal] = None
        self._max_width: typing.Optional[Decimal] = None
        self._preferred_width: typing.Optional[Decimal] = preferred_width

        # height of the TableCell
        self._min_height: typing.Optional[Decimal] = None
        self._max_height: typing.Optional[Decimal] = None
        self._preferred_height: typing.Optional[Decimal] = preferred_height

        # layout
        self._forced_layout_box: typing.Optional[Rectangle] = None

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        if self._forced_layout_box is not None:
            horizontal_border_width: Decimal = Decimal(0)
            if self._border_left:
                horizontal_border_width += self._border_width
            if self._border_right:
                horizontal_border_width += self._border_width

            vertical_border_width: Decimal = Decimal(0)
            if self._border_top:
                vertical_border_width += self._border_width
            if self._border_bottom:
                vertical_border_width += self._border_width

            return Rectangle(
                self._forced_layout_box.get_x()
                + self._padding_left
                + (self._border_width if self._border_left else Decimal(0)),
                self._forced_layout_box.get_y()
                + self._padding_bottom
                + (self._border_width if self._border_bottom else Decimal(0)),
                max(
                    Decimal(0),
                    self._forced_layout_box.get_width()
                    - self._padding_left
                    - self._padding_right
                    - horizontal_border_width,
                ),
                max(
                    Decimal(0),
                    self._forced_layout_box.get_height()
                    - self._padding_top
                    - self._padding_bottom
                    - vertical_border_width,
                ),
            )

        # default
        return self._layout_element.get_layout_box(available_space)

    def _paint_content_box(self, page: "Page", available_space: Rectangle) -> None:
        self._layout_element.paint(page, available_space)

    def _set_layout_box(self, layout_box: Rectangle) -> "TableCell":
        self._forced_layout_box = layout_box
        return self

    #
    # PUBLIC
    #

    def get_column_span(self) -> int:
        """
        This function returns the column span. This specifies the number of columns a cell should span.
        :return:    The column span
        """
        return self._column_span

    def get_layout_box(self, available_space: Rectangle):
        """
        This function returns the previous result of layout
        :return:    the Rectangle that was the result of the previous layout operation
        """
        if self._forced_layout_box is not None:
            return self._forced_layout_box
        return super(TableCell, self).get_layout_box(available_space)

    def get_layout_element(self) -> LayoutElement:
        """
        This function returns the LayoutElement in this TableCell
        :return:    the LayoutElement inside this TableCell
        """
        return self._layout_element

    def get_max_width(self) -> typing.Optional[Decimal]:
        """
        This function returns the maximum width this TableCell (determined by the LayoutElement inside it).
        This function returns None if the maximum width has not yet been determined.
        :return:    the maximum width of this TableCell
        """
        return self._max_width

    def get_max_height(self) -> typing.Optional[Decimal]:
        """
        This function returns the maximum height this TableCell (determined by the LayoutElement inside it).
        This function returns None if the maximum height has not yet been determined.
        :return:    the maximum height of this TableCell
        """
        return self._max_height

    def get_min_width(self) -> typing.Optional[Decimal]:
        """
        This function returns the minimum width this TableCell (determined by the LayoutElement inside it).
        This function returns None if the minimum width has not yet been determined.
        :return:    the minimum width of this TableCell
        """
        return self._min_width

    def get_min_height(self) -> typing.Optional[Decimal]:
        """
        This function returns the minimum height this TableCell (determined by the LayoutElement inside it).
        This function returns None if the minimum height has not yet been determined.
        :return:    the minimum height of this TableCell
        """
        return self._min_height

    def get_preferred_height(self) -> typing.Optional[Decimal]:
        """
        This function returns the preferred height of this TableCell (determined by a previous run of the LayoutElement framework).
        This function returns None if the preferred height has not yet been determined.
        :return:    the preferred height of this TableCell
        """
        return self._preferred_height

    def get_preferred_width(self) -> typing.Optional[Decimal]:
        """
        This function returns the preferred width of this TableCell (determined by a previous run of the LayoutElement framework).
        This function returns None if the preferred width has not yet been determined.
        :return:    the preferred width of this TableCell
        """
        return self._preferred_width

    def get_previous_layout_box(self) -> typing.Optional[Rectangle]:
        """
        This function returns the previous result of layout of this LayoutElement
        :return:    the Rectangle that was the result of the previous layout operation
        """
        return self._layout_element.get_previous_layout_box()

    def get_row_span(self) -> int:
        """
        This function returns the row span. This specifies the number of rows a cell should span.
        :return:    The row span
        """
        return self._row_span

    def get_table_coordinates(self) -> typing.List[typing.Tuple[int, int]]:
        """
        This function returns the coordinates (in the Table) of this TableCell.
        These coordinates may be a single typing.Tuple[int, int] or a typing.List of such
        tuples in case of row/column span.
        :return:    the table coordinates
        """
        return self._table_coordinates


class Table(LayoutElement):
    """
    This class represents a common base for all LayoutElement implementations
    that attempt to represent tabular data.
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
        super(Table, self).__init__(
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
            font_size=Decimal(12),
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
        assert number_of_rows >= 1
        assert number_of_columns >= 1
        self._number_of_rows = number_of_rows
        self._number_of_columns = number_of_columns
        self._content: typing.List[TableCell] = []

    #
    # PRIVATE
    #

    def _get_cells_at(self, row: int, column: int) -> typing.Optional[TableCell]:
        for t in self._content:
            if (
                len(
                    [
                        p
                        for p in t.get_table_coordinates()
                        if p[0] == row and p[1] == column
                    ]
                )
                > 0
            ):
                return t
        return None

    #
    # PUBLIC
    #

    def add(self, layout_element: LayoutElement) -> "Table":
        """
        This function adds the given LayoutElement to this Table.
        This function returns self.
        :param layout_element:  the LayoutElement to be added
        :return:                self
        """

        # embed LayoutElement in TableCell (if needed)
        if not isinstance(layout_element, TableCell):
            layout_element = TableCell(layout_element)

        # add content
        assert isinstance(layout_element, TableCell)
        self._content.append(layout_element)

        # set font_size
        inner_layout_element: LayoutElement = layout_element.get_layout_element()
        if self._font_size is None:
            self._font_size = inner_layout_element.get_font_size()

        # determine gridpoints occupied by the new TableCell
        first_incomplete_row: int = min(
            [
                x
                for x in range(0, self._number_of_rows)
                if sum([y.get_column_span() for y in self.get_cells_at_row(x)])
                < self._number_of_columns
            ]
        )
        # check which columns are already occupied in the current row
        occupied_cols_in_row: typing.List[int] = []
        for c in self.get_cells_at_row(first_incomplete_row):
            occupied_cols_in_row.extend(
                [
                    x[1]
                    for x in c.get_table_coordinates()
                    if x[0] == first_incomplete_row
                ]
            )
        # the first empty column is the lowest number that does not appear in occupied_cols_in_row
        first_empty_column: int = min(
            [
                x
                for x in range(0, self._number_of_columns)
                if x not in occupied_cols_in_row
            ]
        )

        # set _table_coordinates
        for i in range(0, layout_element.get_row_span()):
            for j in range(0, layout_element.get_column_span()):
                layout_element._table_coordinates.append(
                    (first_incomplete_row + i, first_empty_column + j)
                )

        # return
        return self

    def even_odd_row_colors(
        self,
        even_row_color: Color,
        odd_row_color: Color,
        header_row_color: typing.Optional[Color] = None,
    ) -> "Table":
        """
        This function colors the Table with the classic "zebra stripes"
        e.a. one color for all even rows, and a contrasting color for the odd rows.
        This function returns self.
        :param even_row_color:      the Color to be used for even rows
        :param odd_row_color:       the Color to be used for odd rows
        :param header_row_color:    the Color to be used for the header row, if None is specified the even_row_color will be used
        :return:                    self
        """
        if header_row_color is None:
            header_row_color = even_row_color
        assert header_row_color is not None
        for r in range(0, self._number_of_rows):
            for tc in self.get_cells_at_row(r):
                if r == 0:
                    tc._background_color = header_row_color
                else:
                    if r % 2 == 0:
                        tc._background_color = even_row_color
                    else:
                        tc._background_color = odd_row_color
        return self

    def get_cells_at_column(self, column: int) -> typing.List[TableCell]:
        """
        This function returns all TableCell elements at a given column
        :param column:  the specified column
        :return:        all TableCell elements at the given column
        """
        out: typing.List[TableCell] = []
        for t in self._content:
            if len([p for p in t.get_table_coordinates() if p[1] == column]) > 0:
                out.append(t)
        return out

    def get_cells_at_row(self, row: int) -> typing.List[TableCell]:
        """
        This function returns all TableCell elements at a given row
        :param row:  the specified row
        :return:        all TableCell elements at the given row
        """
        out: typing.List[TableCell] = []
        for t in self._content:
            if len([p for p in t.get_table_coordinates() if p[0] == row]) > 0:
                out.append(t)
        return out

    def get_number_of_columns(self) -> int:
        """
        This function returns the number of columns in this Table
        :return:    the number of columns
        """
        return self._number_of_columns

    def get_number_of_rows(self) -> int:
        """
        This function returns the number of rows in this Table
        :return:    the number of rows
        """
        return self._number_of_rows

    def internal_borders(self) -> "Table":
        """
        This method sets the border(s) on all TableCell objects in this Table
        except for the borders that form the outside edge of the Table
        :return:    self
        """
        for tc in self._content:
            tc._border_top = True
            tc._border_right = True
            tc._border_bottom = True
            tc._border_left = True
        for c in self.get_cells_at_row(0):
            c._border_top = False
        for c in self.get_cells_at_row(self._number_of_rows - 1):
            c._border_bottom = False
        for c in self.get_cells_at_column(0):
            c._border_left = False
        for c in self.get_cells_at_column(self._number_of_columns - 1):
            c._border_right = False
        return self

    def no_borders(self) -> "Table":
        """
        This method unsets the border(s) on all TableCell objects in this Table
        :return:    self
        """
        self.set_borders_on_all_cells(False, False, False, False)
        return self

    def outer_borders(self) -> "Table":
        """
        This method unsets the border(s) on all TableCell objects in this Table
        except for the borders that form the outside edge of the Table
        :return:    self
        """
        self.no_borders()
        for c in self.get_cells_at_row(0):
            c._border_top = True
        for c in self.get_cells_at_row(self._number_of_rows - 1):
            c._border_bottom = True
        for c in self.get_cells_at_column(0):
            c._border_left = True
        for c in self.get_cells_at_column(self._number_of_columns - 1):
            c._border_right = True
        return self

    def outer_borders_rounded(self, border_radius: Decimal = Decimal(20)) -> "Table":
        """
        This function sets rounded borders on the outside of this Table
        :param border_radius:   the desired border radius
        :return:                self
        """
        # upper left
        ul: typing.Optional[TableCell] = self._get_cells_at(0, 0)
        if ul is not None:
            ul._border_radius_top_left = border_radius
        # upper right
        ur: typing.Optional[TableCell] = self._get_cells_at(
            0, self._number_of_columns - 1
        )
        if ur is not None:
            ur._border_radius_top_right = border_radius
        # lower right
        lr: typing.Optional[TableCell] = self._get_cells_at(
            self._number_of_rows - 1, self._number_of_columns - 1
        )
        if lr is not None:
            lr._border_radius_bottom_right = border_radius
        # lower left
        ll: typing.Optional[TableCell] = self._get_cells_at(self._number_of_rows - 1, 0)
        if ll is not None:
            ll._border_radius_bottom_left = border_radius
        # return
        return self

    def set_background_color_on_all_cells(self, background_color: Color) -> "Table":
        """
        This method sets the background Color on all TableCell objects in this Table
        :param background_color:    the background Color
        :return:    self
        """
        for e in self._content:
            e._background_color = background_color
        return self

    def set_border_color_on_all_cells(self, border_color: Color) -> "Table":
        """
        This method sets the border color on all TableCell objects in this Table
        :param border_color:    the border Color
        :return:                self
        """
        for e in self._content:
            e._border_color = border_color
        return self

    def set_border_width_on_all_cells(self, border_width: Decimal) -> "Table":
        """
        This method sets the border width on all TableCell objects in this Table
        :param border_width:    the border width
        :return:                self
        """
        assert border_width >= 0
        for e in self._content:
            e._border_width = border_width
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
        :param border_top:          True if a top border should be drawn, False otherwise
        :param border_right:        True if a right border should be drawn, False otherwise
        :param border_bottom:       True if a bottom border should be drawn, False otherwise
        :param border_left:         True if a left border should be drawn, False otherwise
        :return:                    self
        """
        for e in self._content:
            e._border_top = border_top
            e._border_right = border_right
            e._border_bottom = border_bottom
            e._border_left = border_left
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
        :param padding_top:     the top padding
        :param padding_right:   the right padding
        :param padding_bottom:  the bottom padding
        :param padding_left:    the left padding
        :return:                self
        """
        for e in self._content:
            e._padding_top = padding_top
            e._padding_right = padding_right
            e._padding_bottom = padding_bottom
            e._padding_left = padding_left
        return self
