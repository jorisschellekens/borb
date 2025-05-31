import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestFlexibleColumnWidthTableNoBorders(unittest.TestCase):

    def test_flexible_column_width_table_no_borders(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .append_layout_element(
                Paragraph(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                )
            )
            .append_layout_element(
                Paragraph(
                    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                )
            )
            .append_layout_element(
                Paragraph(
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
                )
            )
            .append_layout_element(
                Paragraph(
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                )
            )
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).no_borders().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_flexible_column_width_table_no_borders.pdf"
        )
