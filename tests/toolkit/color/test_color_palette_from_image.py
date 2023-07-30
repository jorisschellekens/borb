import typing
from decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import Image
from borb.pdf.canvas.color.color import Color
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
from tests.test_case import TestCase


class TestColorPaletteFromImage(TestCase):
    def test_extract_color_palette_from_image(self):

        d: Document = Document()

        p: Page = Page()
        d.add_page(p)

        l: PageLayout = SingleColumnLayout(p)

        # add test information
        l.add(
            self.get_test_header(
                test_description="This test creates a PDF with droplet shapes in it, "
                "in colors that originate from an image."
            )
        )

        image_url: str = "https://images.unsplash.com/photo-1674159438102-b2167a502697"
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
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, d)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
