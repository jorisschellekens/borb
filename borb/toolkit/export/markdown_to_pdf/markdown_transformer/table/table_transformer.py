#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles tables
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import Table, TableCell
from borb.toolkit.export.markdown_to_pdf.markdown_transformer.base_markdown_transformer import (
    BaseMarkdownTransformer,
    MarkdownTransformerState,
)


class TableTransformer(BaseMarkdownTransformer):
    """
    This implementation of BaseMarkdownTransformer handles tables
    """

    def _can_transform(self, context: MarkdownTransformerState) -> bool:
        i: int = context.tell()
        while (
            i < len(context.get_markdown_string())
            and context.get_markdown_string()[i] == " "
        ):
            i += 1
        if (
            i >= len(context.get_markdown_string())
            or context.get_markdown_string()[i] != "|"
        ):
            return False
        next_newline_pos: int = context.get_markdown_string().find("\n", i)
        if next_newline_pos == -1:
            next_newline_pos = len(context.get_markdown_string())
        if context.get_markdown_string()[next_newline_pos - 1] == "|":
            return True
        return False

    def _is_alignment_td(self, td: str) -> bool:
        td_stripped: str = td.strip()
        if all([x == "-" for x in td_stripped]):
            return True
        if td_stripped.startswith(":") and all([x == "-" for x in td_stripped[1:]]):
            return True
        if td_stripped.endswith(":") and all([x == "-" for x in td_stripped[:-1]]):
            return True
        if (
            td_stripped.startswith(":")
            and td_stripped.endswith(":")
            and all([x == "-" for x in td_stripped[1:-1]])
        ):
            return True
        return False

    def _transform(self, context: MarkdownTransformerState) -> None:

        # continue processing lines until we hit <newline><newline>
        end_pos: int = self._until_double_newline(context)
        if end_pos == -1:
            end_pos = len(context.get_markdown_string())
        table_lines_raw: typing.List[str] = context.get_markdown_string()[
            context.tell() : end_pos - 1
        ].split("\n")

        index: int = 0
        number_of_columns: int = len(table_lines_raw[0].split("|")) - 2
        column_alignment: typing.List[Alignment] = [
            Alignment.LEFT for _ in range(0, number_of_columns)
        ]
        table_items_str: typing.List[typing.List[str]] = []
        while index < len(table_lines_raw):
            # process alignment line
            if all(
                [self._is_alignment_td(x) for x in table_lines_raw[index].split("|")]
            ):
                for i, a in enumerate(table_lines_raw[index].strip().split("|")[1:-1]):
                    a = a.strip()
                    if a.endswith(":") and a.startswith(":"):
                        column_alignment[i] = Alignment.CENTERED
                    elif a.endswith(":"):
                        column_alignment[i] = Alignment.RIGHT
                index += 1
                continue
            # process normal lines
            table_items_str.append(table_lines_raw[index].strip().split("|")[1:-1])
            index += 1

        # build Table
        number_of_rows: int = len(table_items_str)
        ul: Table = FlexibleColumnWidthTable(
            number_of_columns=number_of_columns, number_of_rows=number_of_rows
        )
        for tr in table_items_str:
            for td in tr:
                sub_context: MarkdownTransformerState = MarkdownTransformerState(td)
                sub_context._document = context._document
                sub_context._parent_layout_element = ul
                self.get_root()._transform(sub_context)

        # set alignment
        for i in range(0, number_of_columns):
            for td_table_cell in ul._get_cells_at_column(i):
                td_table_cell._horizontal_alignment = column_alignment[i]

        # set header row
        for td_table_cell in ul._get_cells_at_row(0):
            td_table_cell._layout_element._font = StandardType1Font("Helvetica-Bold")  # type: ignore [attr-defined]

        # set padding and zebra striping
        ul.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        # ul.even_odd_row_colors(HexColor("ffffff"), HexColor("c3c3c3"))

        # add
        context.get_parent_layout_element().add(ul)  # type: ignore [union-attr]

        # seek
        context.seek(end_pos + 1)
