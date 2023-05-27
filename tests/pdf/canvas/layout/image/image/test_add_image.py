from _decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import Image
from borb.pdf import OrderedList
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import UnorderedList
from tests.test_case import TestCase


class TestAddImage(TestCase):

    IMAGE_URL: str = (
        "https://github.com/jorisschellekens/borb/blob/master/logo/borb_64.png?raw=true"
    )

    def test_add_image(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a Image in it.")
        )
        page_layout.add(Image(TestAddImage.IMAGE_URL))

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_orderedlist_of_images(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an OrderedList of Images in it."
            )
        )
        page_layout.add(
            OrderedList()
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
        )

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_unorderedlist_of_images(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an UnorderedList of Images in it."
            )
        )
        page_layout.add(
            UnorderedList()
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
        )

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_table_of_images(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an Table of Images in it."
            )
        )
        page_layout.add(
            FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3)
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
            .add(Image(TestAddImage.IMAGE_URL))
        )

        # write
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_image_using_borders(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a Image in it.")
        )
        page_layout.add(
            Image(
                TestAddImage.IMAGE_URL,
                border_top=True,
                border_right=True,
                border_bottom=True,
                border_left=True,
                border_color=HexColor("56cbf9"),
                border_radius_top_left=Decimal(10),
                border_radius_top_right=Decimal(10),
                border_radius_bottom_right=Decimal(10),
            )
        )

        # write
        with open(self.get_fifth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_image_using_horizontal_alignment_left(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with a Image in it with horizontal aligmnent set to LEFT."
            )
        )
        page_layout.add(
            Image(TestAddImage.IMAGE_URL, horizontal_alignment=Alignment.LEFT)
        )

        # write
        with open(self.get_sixth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_image_using_horizontal_alignment_centered(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with a Image in it with horizontal aligmnent set to CENTERED."
            )
        )
        page_layout.add(
            Image(TestAddImage.IMAGE_URL, horizontal_alignment=Alignment.CENTERED)
        )

        # write
        with open(self.get_seventh_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_add_image_using_horizontal_alignment_right(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with a Image in it with horizontal aligmnent set to RIGHT."
            )
        )
        page_layout.add(
            Image(TestAddImage.IMAGE_URL, horizontal_alignment=Alignment.RIGHT)
        )

        # write
        with open(self.get_eight_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())
