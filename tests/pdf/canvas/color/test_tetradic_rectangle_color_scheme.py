import datetime
import typing
import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.pantone import Pantone

from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable

from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout

from borb.pdf.canvas.layout.text.paragraph import Paragraph

from borb.pdf.pdf import PDF

from borb.pdf.canvas.geometry.rectangle import Rectangle

from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory

from borb.pdf.canvas.layout.image.shape import Shape

from borb.pdf.canvas.color.color import HexColor, HSVColor, Color

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout

from borb.pdf.page.page import Page

from borb.pdf.document import Document
from tests.test_util import compare_visually_to_ground_truth


class TestTetradicRectangleColorScheme(unittest.TestCase):
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

    def test_triadic_color_scheme(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        # add test information
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with 3 droplet shapes in it, in colors that form a tetradic rectangle."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        cs: typing.List[Color] = HSVColor.tetradic_rectangle(HexColor("f1cd2e"))

        t: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_rows=5, number_of_columns=3, margin_top=Decimal(12)
        )
        t.add(Paragraph("Color Sample", font="Helvetica-Bold"))
        t.add(Paragraph("Hex code", font="Helvetica-Bold"))
        t.add(Paragraph("Nearest Pantone", font="Helvetica-Bold"))
        for c in cs:
            t.add(
                Shape(
                    LineArtFactory.droplet(
                        Rectangle(Decimal(0), Decimal(0), Decimal(32), Decimal(32))
                    ),
                    stroke_color=c,
                    fill_color=c,
                )
            )
            t.add(Paragraph(c.to_rgb().to_hex_string()))
            t.add(Paragraph(Pantone.find_nearest_pantone_color(c).get_name()))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        l.add(t)

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf")
