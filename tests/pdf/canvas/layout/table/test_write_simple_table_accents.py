import logging
import unittest
from pathlib import Path

from ptext.pdf.canvas.font.font import Font

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from ptext.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
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
        font: Font = TrueTypeFont.true_type_font_from_file(
            Path(__file__).parent / "Pacifico.ttf"
        )
        t.add(Paragraph("a", font=font))
        t.add(Paragraph("A", font=font))
        t.add(Paragraph("á", font=font))
        t.add(Paragraph("Á", font=font))
        # B
        t.add(Paragraph("b", font=font))
        t.add(Paragraph("B", font=font))
        t.add(Paragraph("-", font=font))
        t.add(Paragraph("-", font=font))
        # C
        t.add(Paragraph("c", font=font))
        t.add(Paragraph("C", font=font))
        t.add(Paragraph("-", font=font))
        t.add(Paragraph("-", font=font))
        # D
        t.add(Paragraph("d", font=font))
        t.add(Paragraph("D", font=font))
        t.add(Paragraph("-", font=font))
        t.add(Paragraph("-", font=font))
        # E
        t.add(Paragraph("e", font=font))
        t.add(Paragraph("E", font=font))
        t.add(Paragraph("é", font=font))
        t.add(Paragraph("É", font=font))
        # F
        t.add(Paragraph("f", font=font))
        t.add(Paragraph("F", font=font))
        t.add(Paragraph("-", font=font))
        t.add(Paragraph("-", font=font))
        # G
        t.add(Paragraph("g", font=font))
        t.add(Paragraph("G", font=font))
        t.add(Paragraph("-", font=font))
        t.add(Paragraph("-", font=font))
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
        t.add(Paragraph("z", font=font))
        t.add(Paragraph("Z", font=font))
        t.add(Paragraph("-", font=font))
        t.add(Paragraph("-", font=font))

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
