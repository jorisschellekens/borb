import random
import typing

from borb.io.read.types import Decimal
from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.geometry.rectangle import Rectangle
from tests.test_case import TestCase


class TestGoldenRatioLandscapeBox(TestCase):
    def test_get_golden_ratio_landscape_box(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with a (golden ratio sized) Paragraph in it."
            )
        )

        # seed random (to ensure we always get the same Lipsum)
        random.seed(0)

        # generate Paragraph
        p: Paragraph = Paragraph(
            Lipsum.generate_lipsum_text(5), text_alignment=Alignment.JUSTIFIED
        )

        # get_golden_ratio_landscape_box
        r0: typing.Optional[Rectangle] = p.get_golden_ratio_landscape_box()
        assert r0 is not None

        # center
        r1: Rectangle = Rectangle(
            page.get_page_info().get_width() / 2 - r0.get_width() / 2,
            page.get_page_info().get_height() / 2 - r0.get_height() / 2,
            r0.get_width(),
            r0.get_height(),
        )

        # add to Page
        p.paint(page, r1)

        # add debug stats to Page
        page_layout.add(
            Paragraph(
                f"The Paragraph below achieves a ratio of {round(r0.get_width()/r0.get_height(), 2)}. "
                f"Its width is {round(r0.get_width(), 2)}, and its height is {round(r0.get_height(), 2)}."
            )
        )

        # determine output location
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_get_golden_ratio_landscape_box_with_border(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with a (golden ratio sized) Paragraph in it."
            )
        )

        # seed random (to ensure we always get the same Lipsum)
        random.seed(0)

        # generate Paragraph
        p: Paragraph = Paragraph(
            Lipsum.generate_agatha_christie_text(5),
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            border_width=Decimal(1),
            border_color=HexColor("56cbf9"),
            text_alignment=Alignment.JUSTIFIED,
        )

        # get_golden_ratio_landscape_box
        r0: typing.Optional[Rectangle] = p.get_golden_ratio_landscape_box()
        assert r0 is not None

        # center
        r1: Rectangle = Rectangle(
            page.get_page_info().get_width() / 2 - r0.get_width() / 2,
            page.get_page_info().get_height() / 2 - r0.get_height() / 2,
            r0.get_width(),
            r0.get_height(),
        )

        # add to Page
        p.paint(page, r1)

        # add debug stats to Page
        page_layout.add(
            Paragraph(
                f"The Paragraph below achieves a ratio of {round(r0.get_width()/r0.get_height(), 2)}. "
                f"Its width is {round(r0.get_width(), 2)}, and its height is {round(r0.get_height(), 2)}."
            )
        )

        # determine output location
        with open(self.get_second_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())
