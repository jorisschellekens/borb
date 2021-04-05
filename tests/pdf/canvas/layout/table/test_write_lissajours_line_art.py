import logging
import unittest
from pathlib import Path

from ptext.pdf.canvas.layout.shape import Shape

from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color, HSVColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-lissajours-line-art.log"),
    level=logging.DEBUG,
)


class TestWriteFlowchartLineArt(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-lissajours-line-art")

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

        # title
        layout.add(
            Paragraph(
                "Lissajours Line Art",
                font_size=Decimal(20),
                font_color=X11Color("Blue"),
            )
        )

        # table
        N = 7
        fill_colors = [
            HSVColor(Decimal(x / N), Decimal(1), Decimal(1)) for x in range(0, N)
        ]
        stroke_colors = [HSVColor.darker(x) for x in fill_colors]
        fixed_bb = Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100))
        t = Table(number_of_rows=N, number_of_columns=N)
        for i in range(0, N):
            for j in range(0, N):
                t.add(
                    Shape(
                        LineArtFactory.lissajours(fixed_bb, i + 1, j + 1),
                        fill_color=fill_colors[(i + j) % N],
                        stroke_color=stroke_colors[(i + j) % N],
                        line_width=Decimal(2),
                    )
                )

        t.set_padding_on_all_cells(Decimal(10), Decimal(10), Decimal(10), Decimal(10))
        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
