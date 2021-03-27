import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-table-3-rows-layout-fail.log"),
    level=logging.DEBUG,
)


class TestWriteTable3RowsLayoutFail(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-table-3-rows-layout-fail")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)

        t = Table(number_of_rows=3, number_of_columns=2)
        # row 0
        t.add(Paragraph("A"))
        t.add(Paragraph("B"))
        # row 1
        t.add(Paragraph(" ", respect_spaces_in_text=True))
        t.add(Paragraph(" ", respect_spaces_in_text=True))
        # row 2
        t.add(Paragraph(" ", respect_spaces_in_text=True))
        t.add(Paragraph(" ", respect_spaces_in_text=True))

        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
