import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestWriteTableWithSpecialCharacters(unittest.TestCase):
    """
    This test creates a PDF with a Table in it, this Table contains some special (accented) characters.
    """

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
        layout = SingleColumnLayout(page)

        # write test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a Table in it, this Table contains some special (accented) characters."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t = Table(number_of_rows=10, number_of_columns=4, margin_top=Decimal(5))
        t.add(
            Paragraph(
                "lowercase",
                font_color=HexColor("f1cd2e"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "uppercase",
                font_color=HexColor("f1cd2e"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "lowercase acute",
                font_color=HexColor("f1cd2e"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "uppercase acute",
                font_color=HexColor("f1cd2e"),
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
                text="**These are the characters borb can currently render in a PDF",
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
