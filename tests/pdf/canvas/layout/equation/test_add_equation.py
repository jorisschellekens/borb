import unittest

from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.equation.equation import Equation
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddEquation(TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def test_add_equation_addition(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with an equation in it.")
        )
        page_layout.add(Equation("1+2"))

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_equation_divide_by(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with an equation in it.")
        )
        page_layout.add(Equation("sin(x)/cos(x)"))

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_equation_multiplication(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with an equation in it.")
        )
        page_layout.add(Equation("sin(x)*sin(x)"))

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_equation_equality(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header("This test creates a PDF with an equation in it.")
        )
        page_layout.add(Equation("sin(x)/cos(x)=tan(x)"))

        # write
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())


if __name__ == "__main__":
    unittest.main()
