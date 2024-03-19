#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class contains utility methods for using the Table classes in borb.
"""
import numbers
import typing
from decimal import Decimal

# fmt: off
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph


# fmt: on


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
        background_color: Color = HexColor("ffffff"),
        flexible_column_width: bool = True,
        font_color: Color = HexColor("000000"),
        font_size: Decimal = Decimal(12),
        header_background_color: Color = HexColor("f1f3f4"),
        header_col: bool = False,
        header_font_color: Color = HexColor("000000"),
        header_row: bool = True,
        round_to_n_digits: typing.Optional[int] = None,
    ) -> Table:
        """
        This function creates a Table from a 2D array of (stringable) data
        :param data:                        the data used to populate the Table
        :param background_color:            the background color of cells in the Table
        :param flexible_column_width:       true if a FlexibleColumnWidthTable should be used, false otherwise
        :param font_color:                  the font-color of cells in the Table
        :param font_size:                   the font-size of cells in the Table
        :param header_background_color:     the background color of header cells in the Table
        :param header_col:                  whether there is a header column
        :param header_font_color:           the font-color of header cells in the Table
        :param header_row:                  whether there is a header row
        :param round_to_n_digits:           this value is None if digits should not be rounded, if this value is not None, digits are rounded to this precision
        :return:                            a Table containing the data
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
                        Paragraph(
                            s,
                            font_size=font_size,
                            font="Helvetica-Bold",
                            font_color=header_font_color,
                        ),
                        background_color=header_background_color,
                    )
                else:
                    p = TableCell(
                        Paragraph(
                            s,
                            font_size=font_size,
                            font="Helvetica",
                            font_color=font_color,
                        ),
                        background_color=background_color,
                    )
                t.add(p)

        # padding
        t.set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))

        # return
        return t

    @staticmethod
    def from_pandas_dataframe(
        data: "pandas.DataFrame",  # type: ignore[name-defined]
        background_color: Color = HexColor("ffffff"),
        flexible_column_width: bool = True,
        font_color: Color = HexColor("000000"),
        font_size: Decimal = Decimal(12),
        header_background_color: Color = HexColor("f1f3f4"),
        header_col: bool = False,
        header_font_color: Color = HexColor("000000"),
        header_row: bool = True,
        round_to_n_digits: typing.Optional[int] = None,
    ) -> Table:
        """
        This function creates a Table from a 2D array of a pandas.DataFrame
        :param data:                        the data used to populate the Table
        :param background_color:            the background color of cells in the Table
        :param flexible_column_width:       true if a FlexibleColumnWidthTable should be used, false otherwise
        :param font_color:                  the font-color of cells in the Table
        :param font_size:                   the font-size of cells in the Table
        :param header_background_color:     the background color of header cells in the Table
        :param header_col:                  whether there is a header column
        :param header_font_color:           the font-color of header cells in the Table
        :param header_row:                  whether there is a header row
        :param round_to_n_digits:           this value is None if digits should not be rounded, if this value is not None, digits are rounded to this precision
        :return:                            a Table containing the data
        """
        head: typing.List[typing.List[str]] = [[x for x in data.columns]]
        body: typing.List[typing.List[typing.Any]] = [
            [x for x in row] for row in data.values
        ]
        return TableUtil.from_2d_array(
            head + body,
            background_color=background_color,
            flexible_column_width=flexible_column_width,
            font_color=font_color,
            font_size=font_size,
            header_background_color=header_background_color,
            header_col=header_col,
            header_font_color=header_font_color,
            header_row=header_row,
            round_to_n_digits=round_to_n_digits,
        )
