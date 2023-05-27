from borb.pdf import Document
from borb.pdf import Equation
from borb.pdf import OrderedList
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import UnorderedList
from tests.test_case import TestCase


class TestAddListOfEquations(TestCase):
    def test_add_orderedlist_of_equations(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an OrderedList of Equations in it."
            )
        )
        page_layout.add(
            OrderedList()
            .add(Equation("sin(x)+cos(x)"))
            .add(Equation("sin(x)*cos(x)"))
            .add(Equation("sin(x)/cos(x)=tan(x)"))
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_unorderedlist_of_equations(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an UnorderedList of Equations in it."
            )
        )
        page_layout.add(
            UnorderedList()
            .add(Equation("sin(x)+cos(x)"))
            .add(Equation("sin(x)*cos(x)"))
            .add(Equation("sin(x)/cos(x)=tan(x)"))
        )

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())
