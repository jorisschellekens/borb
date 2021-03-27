import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color, HSVColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-simple-table-with-background.log"),
    level=logging.DEBUG,
)


class TestWriteSimpleTableWithBackground(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-write-simple-table-with-background"
        )

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        t = Table(number_of_rows=20, number_of_columns=20)
        colors = [
            HSVColor(Decimal(x / 360), Decimal(1), Decimal(1))
            for x in range(0, 360, int(360 / 20))
        ]
        for i in range(0, 18 * 20):
            t.add(
                TableCell(
                    Paragraph(" ", respect_spaces_in_text=True),
                    background_color=colors[i % len(colors)],
                )
            )
        for i in range(0, 20):
            t.add(
                TableCell(
                    Paragraph(" ", respect_spaces_in_text=True),
                    background_color=colors[i % len(colors)].darker(),
                )
            )
        for i in range(0, 20):
            t.add(
                TableCell(
                    Paragraph(" ", respect_spaces_in_text=True),
                    background_color=colors[i % len(colors)].darker().darker(),
                )
            )

        t.no_borders()
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        table_rect = t.layout(
            page,
            bounding_box=Rectangle(
                Decimal(20), Decimal(600), Decimal(500), Decimal(200)
            ),
        )

        Paragraph(
            text="Love is love",
            font_size=Decimal(8),
            font_color=X11Color("Gray"),
            horizontal_alignment=Alignment.RIGHT,
        ).layout(
            page,
            bounding_box=Rectangle(
                Decimal(20), table_rect.y - 40, table_rect.width, Decimal(20)
            ),
        )

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
