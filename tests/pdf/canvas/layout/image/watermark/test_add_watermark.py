import random

from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import Watermark
from tests.test_case import TestCase


class TestAddWatermark(TestCase):
    def test_add_watermark_001(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a Watermark in it.")
        )

        random.seed(0)
        for _ in range(0, 5):
            page_layout.add(
                Paragraph(Lipsum.generate_lipsum_text(random.choice([3, 4, 5])))
            )

        # add watermark
        Watermark(text="Joris Schellekens", font_color=HexColor("56cbf9")).paint(
            page, None
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_watermark_002(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a Watermark in it.")
        )

        random.seed(0)
        for _ in range(0, 5):
            page_layout.add(
                Paragraph(Lipsum.generate_lipsum_text(random.choice([3, 4, 5])))
            )

        # add watermark
        Watermark(
            text="Joris Schellekens", angle_in_degrees=0, font_color=HexColor("56cbf9")
        ).paint(page, None)

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_watermark_003(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a Watermark in it.")
        )

        random.seed(0)
        for _ in range(0, 5):
            page_layout.add(
                Paragraph(Lipsum.generate_lipsum_text(random.choice([3, 4, 5])))
            )

        # add watermark
        Watermark(
            text="Joris Schellekens",
            angle_in_degrees=-45,
            font_color=HexColor("56cbf9"),
        ).paint(page, None)

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_watermark_004(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a Watermark in it.")
        )

        random.seed(0)
        for _ in range(0, 5):
            page_layout.add(
                Paragraph(Lipsum.generate_lipsum_text(random.choice([3, 4, 5])))
            )

        # add watermark
        page_layout.add(
            Watermark(
                text="Joris Schellekens",
                angle_in_degrees=45,
                font_color=HexColor("56cbf9"),
            )
        )

        # write
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())
