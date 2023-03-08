#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class contains utility methods for using the Table classes in borb.
"""
import numbers
import typing

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import TableCell, Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph


class TableUtil:
    """
    This class contains utility methods for using the Table classes in borb.
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
    def from_2d_array(
        data: typing.List[typing.List[typing.Any]],
        header_row: bool = True,
        header_col: bool = False,
        round_to_n_digits: typing.Optional[int] = None,
        flexible_column_width: bool = True,
    ) -> Table:
        """
        This function creates a Table from a 2D array of (stringable) data
        :param data:                    the data used to populate the Table
        :param header_row:              whether there is a header row
        :param header_col:              whether there is a header column
        :param round_to_n_digits:       this value is None if digits should not be rounded, if this value is not None, digits are rounded to this precision
        :param flexible_column_width:   true if a FlexibleColumnWidthTable should be used, false otherwise
        :return:                        a Table containing the data
        """

        # get number of rows
        row_count: int = len(data)
        assert row_count > 0, "Table must contain at least 1 row"

        # get number of cols
        col_count: int = len(data[0])
        assert col_count > 0, "Table must contain at least 1 column"
        assert all(
            [len(x) == col_count for x in data]
        ), "All rows must contain the same number of columns"

        # instantiate Table
        t: typing.Optional[Table] = None
        if flexible_column_width:
            t = FlexibleColumnWidthTable(
                number_of_rows=row_count, number_of_columns=col_count
            )
        else:
            t = FixedColumnWidthTable(
                number_of_rows=row_count, number_of_columns=col_count
            )
        assert t is not None

        # add data
        for i in range(0, row_count):
            for j in range(0, col_count):
                # build text
                s: str = ""
                if round_to_n_digits is not None and isinstance(
                    data[i][j], numbers.Number
                ):
                    s = str(round(data[i][j], round_to_n_digits))
                else:
                    s = str(data[i][j])

                # build TableCell
                p: typing.Optional[TableCell] = None
                if (i == 0 and header_row) or (j == 0 and header_col):
                    p = TableCell(
                        Paragraph(s, font_size=Decimal(12), font="Helvetica-Bold"),
                        background_color=HexColor("f1f3f4"),
                    )
                else:
                    p = TableCell(Paragraph(s, font_size=Decimal(12), font="Helvetica"))
                t.add(p)

        # padding
        t.set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))

        # return
        return t
