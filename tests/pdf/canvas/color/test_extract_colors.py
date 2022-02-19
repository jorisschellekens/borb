import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor, RGBColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.shape import Shape
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.color.color_spectrum_extraction import ColorSpectrumExtraction
from tests.test_util import compare_visually_to_ground_truth

unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractColors(unittest.TestCase):
    """
    This test attempts to extract the colors for each PDF in the corpus
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

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a few Paragraphs in it, in different colors."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        for c in ["0B3954", "F1CD2E", "DE6449"]:
            layout.add(
                Paragraph(
                    """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """,
                    font_size=Decimal(10),
                    font_color=HexColor(c),
                )
            )

        layout.add(
            Image(
                "https://images.unsplash.com/photo-1621844061203-3f31a2a7d6ad?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=636&q=80",
                width=Decimal(256),
                height=Decimal(256),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

    def test_extract_colors_from_document(self):

        input_file = self.output_dir / "output_001.pdf"

        colors: typing.List[typing.Tuple[RGBColor, int]] = []
        with open(input_file, "rb") as pdf_file_handle:
            l = ColorSpectrumExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for t in l.get_colors_for_page(0, limit=32):
                colors.append(t)

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF naming the colors in the previously created PDF."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        layout.add(Paragraph(" "))

        t: Table = Table(number_of_rows=11, number_of_columns=3)
        t.add(Paragraph("Color Swatch", font="Helvetica-Bold"))
        t.add(Paragraph("% of Page", font="Helvetica-Bold"))
        t.add(Paragraph("Most Similar X11 Color", font="Helvetica-Bold"))
        number_of_pixels: Decimal = (
            doc.get_page(0).get_page_info().get_width()
            * doc.get_page(0).get_page_info().get_height()
        )
        for c in colors[0:10]:
            t.add(
                TableCell(
                    Shape(
                        points=LineArtFactory.droplet(
                            bounding_box=Rectangle(
                                Decimal(0), Decimal(0), Decimal(32), Decimal(32)
                            )
                        ),
                        stroke_color=c[0],
                        fill_color=c[0],
                        line_width=Decimal(1),
                        horizontal_alignment=Alignment.CENTERED,
                    )
                )
            )
            p: int = round(100 * c[1] / number_of_pixels)
            t.add(Paragraph(str(p)))
            t.add(Paragraph(X11Color.find_nearest_x11_color(c[0]).get_name()))
        t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")


if __name__ == "__main__":
    unittest.main()
