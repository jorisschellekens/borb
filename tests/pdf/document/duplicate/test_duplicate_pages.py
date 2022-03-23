import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestDuplicatePages(unittest.TestCase):
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

    def test_write_document(self):

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
                    "This test creates a PDF. Subsequent tests will duplicate pages in this PDF."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # attempt to store PDF
        with open(self.output_dir / "output_000.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_duplicate_pages_in_pdf(self):

        # attempt to store PDF
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output_000.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # check
        assert doc is not None

        # append duplicate page
        doc.append_page(doc.get_page(0))

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_duplicate_pages_in_pdf_and_add_content_before(self):

        # attempt to store PDF
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output_000.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # check
        assert doc is not None

        # add content
        Paragraph(
            """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """,
            text_alignment=Alignment.JUSTIFIED,
        ).layout(
            doc.get_page(0),
            Rectangle(Decimal(100), Decimal(100), Decimal(200), Decimal(200)),
        )

        # append duplicate page
        doc.append_page(doc.get_page(0))

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_duplicate_pages_in_pdf_and_add_content_after(self):

        # attempt to store PDF
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output_000.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # check
        assert doc is not None

        # append duplicate page
        doc.append_page(doc.get_page(0))

        # add content
        Paragraph(
            """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """,
            text_alignment=Alignment.JUSTIFIED,
        ).layout(
            doc.get_page(0),
            Rectangle(Decimal(100), Decimal(100), Decimal(200), Decimal(200)),
        )

        # attempt to store PDF
        with open(self.output_dir / "output_003.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
