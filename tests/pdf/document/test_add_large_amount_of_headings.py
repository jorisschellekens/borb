import sys
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestAddLargeAmountOfHeadings(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_write_document_001(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with 32 pages, each page containing 10 headings."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        sys.setrecursionlimit(1000)
        N: int = 32
        for i in range(0, N):
            # Create empty Page
            page = Page()

            # Add Page to Document
            pdf.append_page(page)

            # Create PageLayout
            layout = SingleColumnLayout(page)

            # add heading
            for j in range(0, 10):
                layout.add(
                    Heading(
                        f"Page {i}, Heading {j}",
                        font_color=HexColor("13505B"),
                        font_size=Decimal(12),
                    )
                )

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with self.assertRaises(RecursionError) as context:
            with open(out_file, "wb") as in_file_handle:
                PDF.dumps(in_file_handle, pdf)

    def test_write_document_002(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with 32 pages, each page containing 10 headings."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        sys.setrecursionlimit(2048)
        N: int = 32
        for i in range(0, N):
            # Create empty Page
            page = Page()

            # Add Page to Document
            pdf.append_page(page)

            # Create PageLayout
            layout = SingleColumnLayout(page)

            # add heading
            for j in range(0, 10):
                layout.add(
                    Heading(
                        f"Page {i}, Heading {j}",
                        font_color=HexColor("13505B"),
                        font_size=Decimal(12),
                    )
                )

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
