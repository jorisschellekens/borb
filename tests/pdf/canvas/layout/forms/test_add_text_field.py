import unittest
from decimal import Decimal

from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import OrderedList
from borb.pdf import UnorderedList
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.forms.text_field import TextField
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddTextField(TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def test_add_textfield(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a TextField in it.")
        )
        page_layout.add(TextField())

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_orderedlist_of_textfields(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an OrderedList of TextFields in it."
            )
        )
        page_layout.add(
            OrderedList().add(TextField()).add(TextField()).add(TextField())
        )

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_unorderedlist_of_textfields(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an UnorderedList of TextFields in it."
            )
        )
        page_layout.add(
            UnorderedList().add(TextField()).add(TextField()).add(TextField())
        )

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_table_of_textfields(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an Table of TextFields in it."
            )
        )
        page_layout.add(
            FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3)
            .add(TextField())
            .add(TextField())
            .add(TextField())
            .add(TextField())
            .add(TextField())
            .add(TextField())
            .add(TextField())
            .add(TextField())
            .add(TextField())
        )

        # write
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_textfield_using_borders(self):
        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with a TextField in it.")
        )
        page_layout.add(
            TextField(
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


if __name__ == "__main__":
    unittest.main()
