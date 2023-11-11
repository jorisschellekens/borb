import unittest
from decimal import Decimal

from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import OrderedList
from borb.pdf import PageLayout
from borb.pdf import UnorderedList
from borb.pdf.canvas.layout.image.unsplash import Unsplash
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddUnsplashImage(TestCase):
    """
    This test creates a PDF with an unsplash Image in it
    """

    def test_add_unsplash_image(self):

        # set unsplash API key
        try:
            from tests.borb_secrets import populate_keyring

            populate_keyring()
        except:
            pass

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a Checkbox in it.")
        )
        page_layout.add(
            Unsplash.get_image(
                keywords=["dove"], width=Decimal(162), height=Decimal(100)
            )
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_orderedlist_of_unsplash_images(self):

        # set unsplash API key
        try:
            from tests.borb_secrets import populate_keyring

            populate_keyring()
        except:
            pass

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
            .add(
                Unsplash.get_image(
                    keywords=["dove"], width=Decimal(162), height=Decimal(100)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["duck"], width=Decimal(162), height=Decimal(100)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["blackbird"], width=Decimal(162), height=Decimal(100)
                )
            )
        )

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_unorderedlist_of_unsplash_images(self):

        # set unsplash API key
        try:
            from tests.borb_secrets import populate_keyring

            populate_keyring()
        except:
            pass

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
            .add(
                Unsplash.get_image(
                    keywords=["dove"], width=Decimal(162), height=Decimal(100)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["duck"], width=Decimal(162), height=Decimal(100)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["blackbird"], width=Decimal(162), height=Decimal(100)
                )
            )
        )

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_table_of_unsplash_images(self):

        # set unsplash API key
        try:
            from tests.borb_secrets import populate_keyring

            populate_keyring()
        except:
            pass

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
            .add(
                Unsplash.get_image(
                    keywords=["dove"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["duck"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["blackbird"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["flamingo"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["kingfisher"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["hummingbird"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["finch"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["crow"], width=Decimal(81), height=Decimal(50)
                )
            )
            .add(
                Unsplash.get_image(
                    keywords=["owl"], width=Decimal(81), height=Decimal(50)
                )
            )
        )

        # write
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())


if __name__ == "__main__":
    unittest.main()
