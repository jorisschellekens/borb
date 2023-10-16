from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayoutWithOverflow
from tests.test_case import TestCase


class TestSingleColumnLayoutWithOverflow(TestCase):
    def test_singlecolumnlayoutwithoverflow(self):

        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)

        layout: SingleColumnLayoutWithOverflow = SingleColumnLayoutWithOverflow(page)

        table: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_columns=5, number_of_rows=50
        )

        table.add(Paragraph("Header 1", font="Helvetica-bold"))
        table.add(Paragraph("Header 2", font="Helvetica-bold"))
        table.add(Paragraph("Header 3", font="Helvetica-bold"))
        table.add(Paragraph("Header 4", font="Helvetica-bold"))
        table.add(Paragraph("Header 1", font="Helvetica-bold"))

        for i in range(0, 49):
            for j in range(0, 5):
                table.add(Paragraph(f"row {i}, col {j}"))

        layout.add(table)

        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
