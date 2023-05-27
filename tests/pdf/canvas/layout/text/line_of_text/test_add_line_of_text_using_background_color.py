from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from tests.test_case import TestCase


class TestAddLineOfTextUsingBackgroundColor(TestCase):
    def test_add_lineoftext_using_background_color_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a LineOfText to the PDF with background_color 023047"
            )
        )
        layout.add(LineOfText("Lorem Ipsum Dolor", background_color=HexColor("023047")))
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_lineoftext_using_background_color_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a LineOfText to the PDF with background_color FFB703"
            )
        )
        layout.add(LineOfText("Lorem Ipsum Dolor", background_color=HexColor("FFB703")))
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_lineoftext_using_background_color_003(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a LineOfText to the PDF with background_color FB8500"
            )
        )
        layout.add(LineOfText("Lorem Ipsum Dolor", background_color=HexColor("FB8500")))
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_lineoftext_using_background_color_004(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a LineOfText to the PDF with background_color 219EBC"
            )
        )
        layout.add(LineOfText("Lorem Ipsum Dolor", background_color=HexColor("219EBC")))
        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_lineoftext_using_background_color_005(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a LineOfText to the PDF with background_color 8ECAE6"
            )
        )
        layout.add(LineOfText("Lorem Ipsum Dolor", background_color=HexColor("8ECAE6")))
        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())
