import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.shape import Shape
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteLissajoursLineArt(unittest.TestCase):
    """
    This test creates a PDF with a Table of variously parametrized Lissajours figures in it.
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
                    "This test creates a PDF with a Table of variously parametrized Lissajours figures in it."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # table
        N = 7
        fill_colors = [HexColor("f1cd2e"), HexColor("0b3954"), HexColor("56cbf9")]
        stroke_colors = [HexColor("0b3954"), HexColor("f1cd2e"), HexColor("a5ffd6")]
        fixed_bb = Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100))
        t = Table(number_of_rows=N, number_of_columns=N, padding_top=Decimal(5))
        for i in range(0, N):
            for j in range(0, N):
                t.add(
                    Shape(
                        LineArtFactory.lissajours(fixed_bb, i + 1, j + 1),
                        fill_color=fill_colors[(i + j) % len(fill_colors)],
                        stroke_color=stroke_colors[(i + j) % len(stroke_colors)],
                        line_width=Decimal(2),
                        horizontal_alignment=Alignment.CENTERED,
                    ).scale_down(Decimal(32), Decimal(32))
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

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf")
