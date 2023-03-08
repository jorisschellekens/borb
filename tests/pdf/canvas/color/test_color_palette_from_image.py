import datetime
import typing
import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf import Image, Alignment
from borb.pdf.canvas.color.color import HexColor, HSVColor, Color
from borb.pdf.canvas.color.color_palette_from_image import ColorPaletteFromImage
from borb.pdf.canvas.color.pantone import Pantone
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestColorPaletteFromImage(unittest.TestCase):
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

    def test_color_palette_from_image(self):

        d: Document = Document()

        p: Page = Page()
        d.add_page(p)

        l: PageLayout = SingleColumnLayout(p)

        # add test information
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with droplet shapes in it, in colors that originate from an image."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        image_url: str = "https://images.unsplash.com/photo-1674159438102-b2167a502697?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8"
        l.add(
            Image(
                image_url,
                width=Decimal(128),
                height=Decimal(128),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        cs: typing.List[Color] = ColorPaletteFromImage.color_palette_from_image(
            image_url, 7
        )
        t: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_rows=len(cs) + 1, number_of_columns=3, margin_top=Decimal(12)
        )
        t.add(Paragraph("Color Sample", font="Helvetica-Bold"))
        t.add(Paragraph("Hex code", font="Helvetica-Bold"))
        t.add(Paragraph("Nearest Pantone", font="Helvetica-Bold"))
        for c in cs:
            t.add(
                ConnectedShape(
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
        out_file = self.output_dir / "output.pdf"
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
