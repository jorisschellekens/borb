from borb.pdf import Alignment
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

    def test_add_equation_using_horizontal_alignment_left(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an equation in it with horizontal alignment LEFT"
            )
        )
        page_layout.add(
            Equation("sin(x)/cos(x)=tan(x)", horizontal_alignment=Alignment.LEFT)
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_equation_using_horizontal_alignment_middle(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an equation in it with horizontal alignment MIDDLE"
            )
        )
        page_layout.add(
            Equation("sin(x)/cos(x)=tan(x)", horizontal_alignment=Alignment.MIDDLE)
        )

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_equation_using_horizontal_alignment_right(self):

        # create document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                "This test creates a PDF with an equation in it with horizontal alignment RIGHT"
            )
        )
        page_layout.add(
            Equation("sin(x)/cos(x)=tan(x)", horizontal_alignment=Alignment.RIGHT)
        )

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())
