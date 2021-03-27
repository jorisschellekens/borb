import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HSVColor
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Alignment,
)
from ptext.pdf.canvas.layout.shape import Shape
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.canvas.line_art.blob_factory import BlobFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-blobs.log"), level=logging.DEBUG
)


class TestWriteBlobs(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-blobs")

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

        N = 4
        colors = [
            HSVColor(Decimal(x / 360.0), Decimal(1), Decimal(1))
            for x in range(0, 360, int(360 / N))
        ]
        t = Table(number_of_rows=N, number_of_columns=N)
        for i in range(0, N):
            for _ in range(0, N):
                t.add(
                    TableCell(
                        Shape(
                            points=BlobFactory.blob(i + 3),
                            stroke_color=colors[i],
                            fill_color=None,
                            line_width=Decimal(1),
                            horizontal_alignment=Alignment.CENTERED,
                        ).scale_up(Decimal(100), Decimal(100))
                    )
                )
        t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
