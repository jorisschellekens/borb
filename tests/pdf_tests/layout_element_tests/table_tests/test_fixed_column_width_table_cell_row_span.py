import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestFixedColumnWidthTableCellRowSpan(unittest.TestCase):

    def test_fixed_column_width_table_cell_row_span(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .append_layout_element(
                Table.TableCell(
                    Paragraph(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                    ),
                    row_span=2,
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
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_fixed_column_width_table_cell_row_span.pdf"
        )
