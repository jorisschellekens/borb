#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <table> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import Table
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class TableTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <table> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <table> element,
        False otherwise
        """
        return html_element.tag == "table"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <table> tag to its corresponding LayoutElement
        """
        # count number of rows / cols
        tbody_element: ET.Element = next(
            iter([x for x in html_element.getchildren() if x.tag == "tbody"]),
            html_element,
        )
        number_of_rows: int = sum(
            [
                int(x.get("rowspan", "1"))
                for x in tbody_element.getchildren()
                if x.tag == "tr"
            ]
        )
        number_of_cols: int = max(
            [
                sum(
                    [
                        int(y.get("colspan", "1"))
                        for y in x.getchildren()
                        if y.tag == "td"
                    ]
                )
                for x in tbody_element.getchildren()
                if x.tag == "tr"
            ]
        )

        table: Table = FlexibleColumnWidthTable(
            number_of_rows=number_of_rows,
            number_of_columns=number_of_cols,
            padding_top=Decimal(5),
            padding_bottom=Decimal(5),
        )

        for e in html_element.getchildren():
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], table
            )

        # set padding
        table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        # set table border
        border_property: int = int(html_element.get("border", "0"))
        if border_property == 0:
            table.no_borders()

        # tail of html_element should be process by whoever is processing <table>

        # add to parent
        layout_element.add(table)  # type: ignore[union-attr]
