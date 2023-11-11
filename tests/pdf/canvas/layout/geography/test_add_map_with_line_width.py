from decimal import Decimal

from borb.pdf import Document
from borb.pdf import MapOfTheWorld
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from tests.test_case import TestCase


class TestAddMapWithLineWidth(TestCase):
    def test_add_map_with_line_width(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header("This tests creates a PDF with a MapOfTheWorld in it.")
        )
        layout.add(
            MapOfTheWorld()
            .set_line_width(Decimal(0.05))
            .set_line_width(Decimal(2), key="United States of America")
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
