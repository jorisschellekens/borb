from decimal import Decimal

from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import Image
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayoutWithOverflow
from tests.test_case import TestCase


class TestSingleColumnLayoutWithOverflow(TestCase):
    def test_singlecolumnlayoutwithoverflow_with_text(self):

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

    def test_singlecolumnlayoutwithoverflow_with_images(self):

        # create an empty Document
        pdf: Document = Document()

        # create an empty Page
        page: Page = Page()
        pdf.add_page(page)

        # create a SingleColumnLayoutWithOverflow
        layout: SingleColumnLayoutWithOverflow = SingleColumnLayoutWithOverflow(page)

        # decide how many images to add
        number_of_content_rows: int = 5

        # create FixedColumnWidthTable
        table: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_columns=7,
            number_of_rows=number_of_content_rows + 1,
            column_widths=[
                Decimal(2),
                Decimal(6),
                Decimal(1),
                Decimal(2),
                Decimal(1),
                Decimal(2),
                Decimal(1),
            ],
        )

        # Add the table header
        table.add(Paragraph("Name", font="Helvetica-Bold"))
        table.add(Paragraph("Image", font="Helvetica-Bold"))
        table.add(Paragraph("A", font="Helvetica-Bold"))
        table.add(Paragraph("B", font="Helvetica-Bold"))
        table.add(Paragraph("C", font="Helvetica-Bold"))
        table.add(Paragraph("D", font="Helvetica-Bold"))
        table.add(Paragraph("E", font="Helvetica-Bold"))

        image_url: str = "https://images.unsplash.com/photo-1606567595334-d39972c85dbe"

        for i in range(number_of_content_rows):
            table.add(Paragraph(f"row_{i}"))
            table.add(Image(image_url, width=Decimal(180), height=Decimal(156)))
            table.add(Paragraph("a"))
            table.add(Paragraph("b"))
            table.add(Paragraph("c"))
            table.add(Paragraph("d"))
            table.add(Paragraph("e"))

        table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        layout.add(table)

        with open(self.get_second_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
