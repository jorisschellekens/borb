import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HSVColor
from borb.pdf.canvas.color.color import HexColor
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


class TestAddDropletsUsingColorSchemes(TestCase):
    def _build_document_for_color_scheme(
        self, color_scheme_name: str, colors: typing.List[Color]
    ):

        # empty Document
        d: Document = Document()

        # add empty Page
        p: Page = Page()
        d.add_page(p)

        l: PageLayout = SingleColumnLayout(p)

        # add test information
        N: int = len(colors)
        l.add(
            self.get_test_header(
                f"This test creates a PDF with {N} droplet shapes in it, in colors that form an {color_scheme_name} color scheme."
            )
        )

        # build FixedColumnWidthTable
        t: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_rows=len(colors) + 1, number_of_columns=3, padding_top=Decimal(12)
        )
        t.add(Paragraph("Color Sample", font="Helvetica-Bold"))
        t.add(Paragraph("Hex code", font="Helvetica-Bold"))
        t.add(Paragraph("Nearest Pantone", font="Helvetica-Bold"))
        for c in colors:
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

        # return
        return d

    def test_analogous_color_scheme(self):

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._build_document_for_color_scheme(
                    "analogous", HSVColor.analogous(HexColor("f1cd2e"))
                ),
            )

        # compare visually
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_split_complementary_color_scheme(self):

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._build_document_for_color_scheme(
                    "split complementary",
                    HSVColor.split_complementary(HexColor("f1cd2e")),
                ),
            )

        # compare visually
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_tetradic_rectangle_color_scheme(self):

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._build_document_for_color_scheme(
                    "tetradic rectangle",
                    HSVColor.tetradic_rectangle(HexColor("f1cd2e")),
                ),
            )

        # compare visually
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_tetradic_square_color_scheme(self):

        # write
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._build_document_for_color_scheme(
                    "tetradic square", HSVColor.tetradic_square(HexColor("f1cd2e"))
                ),
            )

        # compare visually
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_triadic_color_scheme(self):

        # write
        with open(self.get_fifth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._build_document_for_color_scheme(
                    "tetradic square", HSVColor.triadic(HexColor("f1cd2e"))
                ),
            )

        # compare visually
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())
