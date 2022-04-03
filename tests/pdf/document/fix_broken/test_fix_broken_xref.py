import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


class TestRemovePage(unittest.TestCase):
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

    def test_create_document(self):

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
                    "This test creates a PDF with 1 page. Subsequent tests then screw up the XREF."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

    def test_break_document(self):
        # read input document
        bytes_in: bytes = b""
        with open(self.output_dir / "output_001.pdf", "rb") as pdf_in_file_handle:
            bytes_in = pdf_in_file_handle.read()

        # randomly insert spaces
        with open(self.output_dir / "output_002.pdf", "wb") as pdf_out_file_handle:
            i: int = 0
            while i < len(bytes_in):

                # 1 0 obj
                if (
                    48 <= bytes_in[i] <= 57
                    and bytes_in[i + 1] == 32
                    and 48 <= bytes_in[i + 2] <= 57
                    and bytes_in[i + 3] == 32
                    and bytes_in[i + 4] == 111
                    and bytes_in[i + 5] == 98
                    and bytes_in[i + 6] == 106
                ):
                    pdf_out_file_handle.write(b"\n")
                    pdf_out_file_handle.write(
                        b"% These bytes were added after the document was created.\n"
                    )
                    pdf_out_file_handle.write(
                        b"% This causes the XREF table to be wrong.\n"
                    )
                    pdf_out_file_handle.write(b"\n")
                    pdf_out_file_handle.write(bytes_in[i : i + 7])
                    i += 7
                    continue

                # regular
                pdf_out_file_handle.write(bytes_in[i : i + 1])
                i += 1

    def test_read_broken_document(self):

        # read input document
        doc: typing.Optional[Document] = None
        l: SimpleTextExtraction = SimpleTextExtraction()
        with open(self.output_dir / "output_002.pdf", "rb") as pdf_in_file_handle:
            doc = PDF.loads(pdf_in_file_handle, [l])

        # read info properties
        assert doc.get_document_info().get_producer() == "borb"

        # check number of pages
        assert doc.get_document_info().get_number_of_pages() == 1

        # check text
        txt: str = l.get_text_for_page(0)
        while "\n" in txt:
            txt = txt.replace("\n", " ")
        while "  " in txt:
            txt = txt.replace("  ", " ")
        assert "test_fix_broken_xref" in txt
        assert "Description This test creates a PDF with 1 page." in txt
        assert "Subsequent tests then screw up the XREF." in txt
