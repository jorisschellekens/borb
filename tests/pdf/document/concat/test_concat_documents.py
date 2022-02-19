import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestConcatDocuments(unittest.TestCase):
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
                    "This test creates a PDF. Subsequent tests will concatenate 2 PDF documents to this one."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # attempt to store PDF
        with open(self.output_dir / "output_000.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_concat_documents_by_adding_pages(self):

        # attempt to read PDF
        input_file_000 = self.output_dir / "output_000.pdf"
        doc_000 = None
        with open(input_file_000, "rb") as in_file_handle:
            doc_000 = PDF.loads(in_file_handle)

        # attempt to read PDF
        input_file_001 = Path(__file__).parent / "input_001.pdf"
        doc_001 = None
        with open(input_file_001, "rb") as in_file_handle:
            doc_001 = PDF.loads(in_file_handle)

        # attempt to read PDF
        input_file_002 = Path(__file__).parent / "input_002.pdf"
        doc_002 = None
        with open(input_file_002, "rb") as in_file_handle_b:
            doc_002 = PDF.loads(in_file_handle_b)

        # concat all pages to same document
        doc_003 = Document()
        for i in range(0, int(doc_000.get_document_info().get_number_of_pages())):
            doc_003.append_page(doc_000.get_page(i))
        for i in range(0, int(doc_001.get_document_info().get_number_of_pages())):
            doc_003.append_page(doc_001.get_page(i))
        for i in range(0, int(doc_002.get_document_info().get_number_of_pages())):
            doc_003.append_page(doc_002.get_page(i))

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc_003)

    def test_concat_documents_by_convenience_method(self):

        # attempt to read PDF
        input_file_000 = self.output_dir / "output_000.pdf"
        doc_000 = None
        with open(input_file_000, "rb") as in_file_handle:
            doc_000 = PDF.loads(in_file_handle)

        # attempt to read PDF
        input_file_001 = Path(__file__).parent / "input_001.pdf"
        doc_001 = None
        with open(input_file_001, "rb") as in_file_handle:
            doc_001 = PDF.loads(in_file_handle)

        # attempt to read PDF
        input_file_002 = Path(__file__).parent / "input_002.pdf"
        doc_002 = None
        with open(input_file_002, "rb") as in_file_handle_b:
            doc_002 = PDF.loads(in_file_handle_b)

        doc_000.append_document(doc_001)
        doc_000.append_document(doc_002)

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc_000)
