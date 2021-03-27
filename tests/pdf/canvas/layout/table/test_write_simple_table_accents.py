import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-simple-table-accents.log"),
    level=logging.DEBUG,
)


class TestWriteSimpleTableAccents(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-simple-table-accents")

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

        t = Table(number_of_rows=10, number_of_columns=4)
        t.add(
            Paragraph(
                "lowercase",
                font_color=X11Color("YellowGreen"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "uppercase",
                font_color=X11Color("YellowGreen"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "lowercase acute",
                font_color=X11Color("YellowGreen"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "uppercase acute",
                font_color=X11Color("YellowGreen"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        # A
        t.add(Paragraph("a"))
        t.add(Paragraph("A"))
        t.add(Paragraph("á"))
        t.add(Paragraph("Á"))
        # B
        t.add(Paragraph("b"))
        t.add(Paragraph("B"))
        t.add(Paragraph("-"))
        t.add(Paragraph("-"))
        # C
        t.add(Paragraph("c"))
        t.add(Paragraph("C"))
        t.add(Paragraph("-"))
        t.add(Paragraph("-"))
        # D
        t.add(Paragraph("d"))
        t.add(Paragraph("D"))
        t.add(Paragraph("-"))
        t.add(Paragraph("-"))
        # E
        t.add(Paragraph("e"))
        t.add(Paragraph("E"))
        t.add(Paragraph("é"))
        t.add(Paragraph("É"))
        # F
        t.add(Paragraph("f"))
        t.add(Paragraph("F"))
        t.add(Paragraph("-"))
        t.add(Paragraph("-"))
        # G
        t.add(Paragraph("g"))
        t.add(Paragraph("G"))
        t.add(Paragraph("-"))
        t.add(Paragraph("-"))
        # ..
        t.add(
            Paragraph(
                "...",
                font_color=X11Color("LightGray"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "...",
                font_color=X11Color("LightGray"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "...",
                font_color=X11Color("LightGray"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "...",
                font_color=X11Color("LightGray"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        # Z
        t.add(Paragraph("z"))
        t.add(Paragraph("Z"))
        t.add(Paragraph("-"))
        t.add(Paragraph("-"))

        t.set_border_width_on_all_cells(Decimal(0.2))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout.add(t)

        layout.add(
            Paragraph(
                text="**These are the characters pText can currently render in a PDF",
                font_size=Decimal(8),
                font_color=X11Color("Gray"),
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
