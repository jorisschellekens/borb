from borb.pdf import HexColor
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.equation.equation import Equation
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddEquationUsingFontColor(TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def test_add_equation_using_font_color(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an equation in it with a non-default font_color."
            )
        )
        page_layout.add(Equation("sin(x)/cos(x)=tan(x)", font_color=HexColor("56cbf9")))

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
