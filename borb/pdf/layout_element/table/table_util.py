#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility class for creating and managing tables in PDF documents.

The `TableUtil` class provides helper methods for generating tables from structured data.
It simplifies the process of converting raw tabular data into a table format suitable for use in PDF documents.
This class allows for customization of table appearance, such as font size,
padding, alignment, and the designation of headers.
"""
import typing

from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph


class TableUtil:
    """
    Utility class for creating and managing tables in PDF documents.

    The `TableUtil` class provides helper methods for generating tables from structured data.
    It simplifies the process of converting raw tabular data into a table format suitable for use in PDF documents.
    This class allows for customization of table appearance, such as font size,
    padding, alignment, and the designation of headers.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def from_2d_data(
        tabular_data: typing.List[typing.List[typing.Any]],
        fixed_column_width: int = False,
        font_size: int = 12,
        header_col: bool = False,
        header_row: bool = True,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ) -> "Table":
        """
        Create a `Table` instance from 2D tabular data.

        The `from_2d_data` method is a static method that generates a table from a 2D list of data,
        allowing for customization of font size, alignment, padding,
        and whether the first row or column should be treated as headers.
        This method simplifies the creation of tables for PDF documents
        by converting raw data into a structured table format.

        :param tabular_data:            A 2D list of values where each sublist represents a row of data.
        :param font_size:               The font size for the table text. Default is 12.
        :param header_col:              A boolean indicating if the first column should be treated as a header.
                                        Default is False.
        :param header_row:              A boolean indicating if the first row should be treated as a header.
                                        Default is True.
        :param horizontal_alignment:    Specifies the horizontal alignment of table content.
                                        Can be LEFT, MIDDLE, or RIGHT. Default is LEFT.
        :param padding_bottom:          The amount of padding to apply to the bottom of each cell. Default is 0.
        :param padding_left:            The amount of padding to apply to the left of each cell. Default is 0.
        :param padding_right:           The amount of padding to apply to the right of each cell. Default is 0.
        :param padding_top:             The amount of padding to apply to the top of each cell. Default is 0.
        :param vertical_alignment:      Specifies the vertical alignment of table content.
                                        Can be TOP, MIDDLE, or BOTTOM. Default is TOP.
        :return:                        Self, allowing for method chaining
        """
        nof_rows: int = len(tabular_data)
        nof_cols: int = len(tabular_data[0])
        table: typing.Optional[Table] = None
        if fixed_column_width:
            table = FixedColumnWidthTable(
                number_of_columns=nof_cols,
                number_of_rows=nof_rows,
                padding_top=padding_top,
                padding_right=padding_right,
                padding_bottom=padding_bottom,
                padding_left=padding_left,
                vertical_alignment=vertical_alignment,
                horizontal_alignment=horizontal_alignment,
            )
        else:
            table = FlexibleColumnWidthTable(
                number_of_columns=nof_cols,
                number_of_rows=nof_rows,
                padding_top=padding_top,
                padding_right=padding_right,
                padding_bottom=padding_bottom,
                padding_left=padding_left,
                vertical_alignment=vertical_alignment,
                horizontal_alignment=horizontal_alignment,
            )
        assert table is not None
        for row_index, row in enumerate(tabular_data):
            for col_index, col in enumerate(row):

                # determine whether the TableCell is a header
                is_header: bool = False
                is_header = is_header or (row_index == 0 and header_row)
                is_header = is_header or (col_index == 0 and header_col)

                # determine text
                if isinstance(col, float):
                    col = str(round(col, 2))
                if not isinstance(col, str):
                    col = str(col)

                table.append_layout_element(
                    Table.TableCell(
                        Paragraph(
                            text=col,
                            font_size=(font_size + 2) if is_header else font_size,
                            font=(
                                Standard14Fonts.get("Helvetica-Bold")
                                if is_header
                                else Standard14Fonts.get("Helvetica")
                            ),
                            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                            padding_bottom=int(0.2 * font_size),
                        ),
                        background_color=(
                            X11Color.YELLOW_MUNSELL if is_header else X11Color.WHITE
                        ),
                        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                        vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                    )
                )
        return table
