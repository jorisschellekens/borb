from borb.pdf import Document
from borb.pdf import Heading
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from tests.test_case import TestCase


class TestAddHeadingUsingAccentedCharacters(TestCase):
    def test_add_heading_using_accented_characters(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a Heading to the PDF."
            )
        )

        layout.add(Heading("Dirección Código Número"))
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
