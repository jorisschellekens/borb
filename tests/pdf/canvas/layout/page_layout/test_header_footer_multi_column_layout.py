import random
from decimal import Decimal

from borb.pdf import MultiColumnLayout
from borb.pdf import PageLayout
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.lipsum.lipsum import Lipsum
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestHeaderFooterMultiColumnLayout(TestCase):
    """
    This test creates a PDF with multiple pages.
    """

    def _add_header(self, page: Page, rectangle: Rectangle) -> None:
        Paragraph(
            """
            Joris Schellekens
            borb (ez)
            Belgium
            """,
            font_size=Decimal(10),
            font_color=HexColor("D3D3D3"),
            respect_newlines_in_text=True,
            border_bottom=True,
            border_width=Decimal(2),
        ).paint(page, rectangle)

    def _add_footer(self, page: Page, rectangle: Rectangle) -> None:
        Paragraph(
            """
            page X / Y
            confidential
            """,
            font_size=Decimal(10),
            font_color=HexColor("D3D3D3"),
            respect_newlines_in_text=True,
        ).paint(page, rectangle)

    def test_header_and_footer(self):

        # create document
        pdf = Document()

        # add test information
        page = Page()
        pdf.add_page(page)

        # init layout
        w: Decimal = page.get_page_info().get_width()
        h: Decimal = page.get_page_info().get_height()
        l: PageLayout = MultiColumnLayout(
            page,
            column_widths=[w * Decimal(0.8)],
            margin_top=Decimal(0.1) * h,
            margin_right=Decimal(0.1) * w,
            margin_bottom=Decimal(0.1) * h,
            margin_left=Decimal(0.1) * w,
            header_paint_method=self._add_header,
            footer_paint_method=self._add_footer,
        )

        # add content
        random.seed(0)
        for _ in range(20):
            l.add(Paragraph(Lipsum.generate_lipsum_text(random.choice([4, 5, 6]))))

        # attempt to store PDF
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_set_header(self):

        # create document
        pdf = Document()

        # add test information
        page = Page()
        pdf.add_page(page)

        # init layout
        w: Decimal = page.get_page_info().get_width()
        h: Decimal = page.get_page_info().get_height()
        l: PageLayout = MultiColumnLayout(
            page,
            column_widths=[w * Decimal(0.8)],
            margin_top=Decimal(0.1) * h,
            margin_right=Decimal(0.1) * w,
            margin_bottom=Decimal(0.1) * h,
            margin_left=Decimal(0.1) * w,
            header_paint_method=self._add_header,
        )

        # add content
        random.seed(0)
        for _ in range(20):
            l.add(Paragraph(Lipsum.generate_lipsum_text(random.choice([4, 5, 6]))))

        # attempt to store PDF
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_set_footer(self):

        # create document
        pdf = Document()

        # add test information
        page = Page()
        pdf.add_page(page)

        # init layout
        w: Decimal = page.get_page_info().get_width()
        h: Decimal = page.get_page_info().get_height()
        l: PageLayout = MultiColumnLayout(
            page,
            column_widths=[w * Decimal(0.8)],
            margin_top=Decimal(0.1) * h,
            margin_right=Decimal(0.1) * w,
            margin_bottom=Decimal(0.1) * h,
            margin_left=Decimal(0.1) * w,
            footer_paint_method=self._add_footer,
        )

        # add content
        random.seed(0)
        for _ in range(20):
            l.add(Paragraph(Lipsum.generate_lipsum_text(random.choice([4, 5, 6]))))

        # attempt to store PDF
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())
