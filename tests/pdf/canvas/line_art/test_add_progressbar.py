from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.progressbar import ProgressBar
from borb.pdf.canvas.layout.shape.progressbar import ProgressSquare
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddProgressbar(TestCase):
    """
    This test creates a PDF with a dragon-curve in it.
    """

    def test_add_progressbar(self):

        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with Table of ProgressBars and ProgressSquares in it"
            )
        )

        t: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_columns=3, number_of_rows=12
        )
        t.add(Paragraph("Percentage", font="Helvetica-Bold"))
        t.add(Paragraph("ProgressBar", font="Helvetica-Bold"))
        t.add(Paragraph("ProgressSquare", font="Helvetica-Bold"))
        for i in range(0, 110, 10):
            t.add(Paragraph(str(i)))
            t.add(
                ProgressBar(
                    percentage=i / 100,
                    stroke_color=HexColor("#6F8F72"),
                    fill_color=HexColor("#8FD694"),
                )
            )
            t.add(
                ProgressSquare(
                    percentage=(i / 100),
                    stroke_color=HexColor("#6F8F72"),
                    fill_color=HexColor("#8FD694"),
                )
            )
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        layout.add(t)
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
