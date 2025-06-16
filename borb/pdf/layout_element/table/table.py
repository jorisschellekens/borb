#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a table layout element in a PDF document.

The `Table` class serves as a common superclass for both fixed and flexible
column tables, providing shared functionality and attributes essential for
managing tabular data within PDF documents. This class enables the
organization and presentation of data in a structured format, allowing
for the rendering of complex layouts.
"""
import functools
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page


class Table(LayoutElement):
    """
    Represents a table layout element in a PDF document.

    The `Table` class serves as a common superclass for both fixed and flexible
    column tables, providing shared functionality and attributes essential for
    managing tabular data within PDF documents. This class enables the
    organization and presentation of data in a structured format, allowing
    for the rendering of complex layouts.
    """

    class TableCell(LayoutElement):
        """
        Represents a cell within a table in a PDF document.

        The `TableCell` class is used to define individual cells in a table structure.
        Each cell can contain various layout elements, such as text, images, or other
        graphical components, allowing for rich content presentation within the table.
        """

        #
        # CONSTRUCTOR
        #

        def __init__(
            self,
            e: LayoutElement,
            background_color: typing.Optional[Color] = None,
            border_color: typing.Optional[Color] = X11Color.BLACK,
            border_dash_pattern: typing.List[int] = [],
            border_dash_phase: int = 0,
            border_width_bottom: int = 1,
            border_width_left: int = 1,
            border_width_right: int = 1,
            border_width_top: int = 1,
            column_span: int = 1,
            horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
            margin_bottom: int = 0,
            margin_left: int = 0,
            margin_right: int = 0,
            margin_top: int = 0,
            padding_bottom: int = 0,
            padding_left: int = 0,
            padding_right: int = 0,
            padding_top: int = 0,
            row_span: int = 1,
            vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
        ):
            """
            Initialize the TableCell object with specific attributes for layout and appearance.

            The `TableCell` class represents an individual cell within a table structure,
            allowing for customization of its layout and visual properties.
            This constructor initializes the cell with attributes such as the contained layout element,
            span across columns and rows, background and border colors, margin and padding settings, and alignment options.
            This flexibility makes it suitable for various table designs and presentations.

            :param e:                       The layout element contained within this table cell, typically a visual or textual component.
            :param column_span:             The number of columns that this cell spans. Default is 1.
            :param row_span:                The number of rows that this cell spans. Default is 1.
            :param background_color:        Optional background color for the cell. Default is None.
            :param border_color:            Optional border color for the cell. Default is X11Color.BLACK.
            :param border_dash_pattern:     A list defining the dash pattern for the cell's border. Default is an empty list.
            :param border_dash_phase:       The phase offset for the dash pattern of the cell's border. Default is 0.
            :param border_width_bottom:     Width of the bottom border of the cell. Default is 1.
            :param border_width_left:       Width of the left border of the cell. Default is 1.
            :param border_width_right:      Width of the right border of the cell. Default is 1.
            :param border_width_top:        Width of the top border of the cell. Default is 1.
            :param horizontal_alignment:    Horizontal alignment of the content within the cell. Default is LayoutElement.HorizontalAlignment.LEFT.
            :param margin_bottom:           Bottom margin for spacing around the cell. Default is 0.
            :param margin_left:             Left margin for spacing around the cell. Default is 0.
            :param margin_right:            Right margin for spacing around the cell. Default is 0.
            :param margin_top:              Top margin for spacing around the cell. Default is 0.
            :param padding_bottom:          Padding at the bottom of the cell. Default is 5.
            :param padding_left:            Padding on the left side of the cell. Default is 5.
            :param padding_right:           Padding on the right side of the cell. Default is 5.
            :param padding_top:             Padding at the top of the cell. Default is 5.
            :param vertical_alignment:      Vertical alignment of the content within the cell. Default is LayoutElement.VerticalAlignment.TOP.
            """
            super().__init__(
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
            self.__inner_layout_element: LayoutElement = e
            self.__column_span: int = column_span
            self.__row_span: int = row_span

        #
        # PRIVATE
        #

        #
        # PUBLIC
        #

        def get_column_span(self) -> int:
            """
            Return the number of columns that the table cell spans.

            This method retrieves the column span of the cell, indicating how many columns
            the cell occupies within the table layout.

            :return: The number of columns the cell spans.
            """
            return self.__column_span

        def get_row_span(self) -> int:
            """
            Return the number of rows that the table cell spans.

            This method retrieves the row span of the cell, indicating how many rows
            the cell occupies within the table layout.

            :return: The number of rows the cell spans.
            """
            return self.__row_span

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
            w, h = self.__inner_layout_element.get_size(
                available_space=(
                    available_space[0]
                    - self.get_padding_left()
                    - self.get_padding_right(),
                    available_space[1]
                    - self.get_padding_top()
                    - self.get_padding_bottom(),
                )
            )
            return (
                w + self.get_padding_left() + self.get_padding_right(),
                h + self.get_padding_top() + self.get_padding_bottom(),
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
            self._paint_background_and_borders(page=page, rectangle=available_space)
            self.__inner_layout_element.paint(
                available_space=(
                    available_space[0] + self.get_padding_left(),
                    available_space[1] + self.get_padding_bottom(),
                    available_space[2]
                    - self.get_padding_left()
                    - self.get_padding_right(),
                    available_space[3]
                    - self.get_padding_top()
                    - self.get_padding_top(),
                ),
                page=page,
            )

            # get previous_paint_box
            # fmt: off
            previous_paint_box: typing.Optional[typing.Tuple[int, int, int, int]] = self.__inner_layout_element.get_previous_paint_box()
            assert previous_paint_box is not None
            # fmt: on

            self._LayoutElement__previous_paint_box = (
                previous_paint_box[0] - self.get_padding_left(),
                previous_paint_box[1] - self.get_padding_bottom(),
                previous_paint_box[2]
                + self.get_padding_left()
                + self.get_padding_right(),
                previous_paint_box[3]
                + self.get_padding_top()
                + self.get_padding_bottom(),
            )

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
        Initialize a new `Table` object for rendering a structured table in a PDF document.

        This constructor allows customization of the table's dimensions and appearance,
        including the number of rows and columns, background and border colors, padding,
        and alignment. These properties are essential for defining how the table will be
        presented within the PDF, ensuring a clear and organized layout.

        :param number_of_rows:           The number of rows in the table.
        :param number_of_columns:        The number of columns in the table.
        :param background_color:         Optional background color for the table.
        :param border_color:             Optional border color for the table.
        :param border_dash_pattern:      Dash pattern used for the table's border lines.
        :param border_dash_phase:        Phase offset for the dash pattern in the table borders.
        :param border_width_bottom:      Width of the bottom border of the table.
        :param border_width_left:        Width of the left border of the table.
        :param border_width_right:       Width of the right border of the table.
        :param border_width_top:         Width of the top border of the table.
        :param horizontal_alignment:      Horizontal alignment of the table (default is LEFT).
        :param margin_bottom:            Space between the table and the element below it.
        :param margin_left:              Space between the table and the left page margin.
        :param margin_right:             Space between the table and the right page margin.
        :param margin_top:               Space between the table and the element above it.
        :param padding_bottom:           Padding inside the table at the bottom.
        :param padding_left:             Padding inside the table on the left side.
        :param padding_right:            Padding inside the table on the right side.
        :param padding_top:              Padding inside the table at the top.
        :param vertical_alignment:        Vertical alignment of the table (default is TOP).
        """
        assert number_of_rows > 0
        assert number_of_columns > 0
        self.__number_of_rows: int = number_of_rows
        self.__number_of_columns: int = number_of_columns
        self.__inner_layout_elements: typing.List[Table.TableCell] = []
        self.__inner_layout_element_to_table_coordinates: typing.Dict[
            Table.TableCell, typing.List[typing.Tuple[int, int]]
        ] = {}
        self.__available_table_coordinates: typing.List[typing.Tuple[int, int]] = [
            (i // self.__number_of_columns, i % self.__number_of_columns)
            for i in range(self.__number_of_rows * self.__number_of_columns)
        ]

        super().__init__(
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

    #
    # PUBLIC
    #

    def append_layout_element(self, layout_element: LayoutElement) -> "Table":
        """
        Add a LayoutElement to the table.

        This method appends a specified LayoutElement (such as a TableCell, Row, or other
        layout component) to the table. The element will be positioned according to the
        current table layout rules.

        :param layout_element:   The LayoutElement to be added to the table.
        :return:    The Table instance, allowing for method chaining.
        """
        e2: Table.TableCell = (
            layout_element
            if isinstance(layout_element, Table.TableCell)
            else Table.TableCell(layout_element)
        )
        self.__inner_layout_elements += [e2]

        # assign table grid coordinates
        start_row, start_col = min(
            self.__available_table_coordinates,
            key=lambda x: x[0] * self.__number_of_columns + x[1],
        )
        self.__inner_layout_element_to_table_coordinates[e2] = []
        for r in range(start_row, start_row + e2.get_row_span()):
            for c in range(start_col, start_col + e2.get_column_span()):
                self.__available_table_coordinates.remove((r, c))
                self.__inner_layout_element_to_table_coordinates[e2].append((r, c))

        # return
        return self

    def get_column(self, column: int) -> typing.List[TableCell]:
        """
        Retrieve all cells in the specified column, accounting for column spans.

        This method returns a list of TableCell objects that belong to the specified column.
        It takes into consideration any column spans that may affect the layout, ensuring that
        cells spanning multiple columns are included correctly.

        :param column: The index of the column from which to retrieve the cells (0-based).
        :return: A list of TableCell objects in the specified column, including those
                 that span multiple columns.
        :raises IndexError: If the specified column index is out of bounds.
        """
        return [
            k
            for k, v in self.__inner_layout_element_to_table_coordinates.items()
            if column in [c for _, c in v]
        ]

    def get_row(self, row: int) -> typing.List[TableCell]:
        """
        Retrieve all cells in the specified row, accounting for row spans.

        This method returns a list of TableCell objects that belong to the specified row.
        It considers any row spans that may affect the layout, ensuring that cells
        spanning multiple rows are included correctly.

        :param row: The index of the row from which to retrieve the cells (0-based).
        :return:    A list of TableCell objects in the specified row, including those
                    that span multiple rows.
        :raises IndexError: If the specified row index is out of bounds.
        """
        return [
            k
            for k, v in self.__inner_layout_element_to_table_coordinates.items()
            if row in [r for r, _ in v]
        ]

    def no_borders(self) -> "Table":
        """
        Remove all borders from the table.

        This method sets the border styles of the table and its cells to
        be invisible, providing a clean and borderless appearance. It can
        be useful when a minimalist design is preferred.

        :return:    Self
        """
        for e in self.__inner_layout_elements:
            e._LayoutElement__border_width_bottom = 0  # type: ignore[attr-defined]
            e._LayoutElement__border_width_left = 0  # type: ignore[attr-defined]
            e._LayoutElement__border_width_right = 0  # type: ignore[attr-defined]
            e._LayoutElement__border_width_top = 0  # type: ignore[attr-defined]
            e._LayoutElement__border_color = None  # type: ignore[attr-defined]
        return self

    def no_external_borders(self) -> "Table":
        """
        Disable the drawing of external borders for the table.

        This method removes any external borders from the table, allowing the
        content to blend seamlessly with the surrounding layout. It is useful
        for achieving a cleaner look when external borders are not desired.

        :return: self
        """
        for e, v in self.__inner_layout_element_to_table_coordinates.items():
            if 0 in [r for r, _ in v]:
                e._LayoutElement__border_width_top = 0  # type: ignore[attr-defined]
            if (self.__number_of_columns - 1) in [c for _, c in v]:
                e._LayoutElement__border_width_right = 0  # type: ignore[attr-defined]
            if (self.__number_of_rows - 1) in [r for r, _ in v]:
                e._LayoutElement__border_width_bottom = 0  # type: ignore[attr-defined]
            if 0 in [c for _, c in v]:
                e._LayoutElement__border_width_left = 0  # type: ignore[attr-defined]
        return self

    def no_internal_borders(self) -> "Table":
        """
        Disable the drawing of internal borders for the table.

        This method removes any internal borders from the table, allowing the
        content to blend seamlessly with the surrounding layout. It is useful
        for achieving a cleaner look when internal borders are not desired.

        :return: self
        """
        self.no_borders()
        for e, v in self.__inner_layout_element_to_table_coordinates.items():
            if 0 in [r for r, _ in v]:
                # fmt: off
                e._LayoutElement__border_color = e._LayoutElement__border_color or X11Color.BLACK   # type: ignore[attr-defined]
                e._LayoutElement__border_width_top = 1                                              # type: ignore[attr-defined]
                # fmt: on
            if (self.__number_of_columns - 1) in [c for _, c in v]:
                # fmt: off
                e._LayoutElement__border_color = e._LayoutElement__border_color or X11Color.BLACK   # type: ignore[attr-defined]
                e._LayoutElement__border_width_right = 1                                            # type: ignore[attr-defined]
                # fmt: on
            if (self.__number_of_rows - 1) in [r for r, _ in v]:
                # fmt: off
                e._LayoutElement__border_color = e._LayoutElement__border_color or X11Color.BLACK   # type: ignore[attr-defined]
                e._LayoutElement__border_width_bottom = 1                                           # type: ignore[attr-defined]
                # fmt: on
            if 0 in [c for _, c in v]:
                # fmt: off
                e._LayoutElement__border_color = e._LayoutElement__border_color or X11Color.BLACK   # type: ignore[attr-defined]
                e._LayoutElement__border_width_left = 1                                             # type: ignore[attr-defined]
                # fmt: on
        return self

    def set_padding_on_all_cells(
        self,
        padding_bottom: int,
        padding_left: int,
        padding_right: int,
        padding_top: int,
    ) -> "Table":
        """
        Set the padding for all cells in the table.

        This method applies the specified padding values to all cells in the table,
        affecting the space between the content of each cell and its boundary.
        The padding is applied individually for each side: top, bottom, left, and right.

        :param padding_bottom:  The amount of padding (in pixels) to apply to the bottom of each cell.
        :param padding_left:    The amount of padding (in pixels) to apply to the left side of each cell.
        :param padding_right:   The amount of padding (in pixels) to apply to the right side of each cell.
        :param padding_top:     The amount of padding (in pixels) to apply to the top of each cell.
        :return:                Self, allowing for method chaining
        """
        for e in self.__inner_layout_elements:
            e._LayoutElement__padding_bottom = padding_bottom  # type: ignore[attr-defined]
            e._LayoutElement__padding_left = padding_left  # type: ignore[attr-defined]
            e._LayoutElement__padding_right = padding_right  # type: ignore[attr-defined]
            e._LayoutElement__padding_top = padding_top  # type: ignore[attr-defined]
        return self

    def striped(
        self,
        even_row_color: typing.Optional[Color] = X11Color.LIGHT_GRAY,
        odd_row_color: typing.Optional[Color] = None,
    ) -> "Table":
        """
        Apply a striped color pattern to the rows of the table.

        This method sets the background colors for even and odd rows in the
        table to enhance readability. By default, even rows are colored
        light gray, while odd rows can be set to a custom color. If no color
        is provided for odd rows, they will remain uncolored.
        :param even_row_color:  The background color for even rows. Defaults to X11Color.LIGHT_GRAY.
        :param odd_row_color:   The background color for odd rows. Defaults to None.
        """
        for i in range(0, self.__number_of_rows):
            c: typing.Optional[Color] = (
                even_row_color if (i % 2 == 0) else odd_row_color
            )
            for e in self.get_row(i):
                e._LayoutElement__background_color = c  # type: ignore[attr-defined]
        return self
