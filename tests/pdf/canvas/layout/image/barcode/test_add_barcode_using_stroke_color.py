from _decimal import Decimal

from borb.pdf import Barcode
from borb.pdf import BarcodeType
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from tests.test_case import TestCase


class TestAddBarcodeUsingStrokeColor(TestCase):
    def test_add_barcode_using_stroke_color(self):

        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                test_description=f"This test creates a PDF with a Barcode in it."
            )
        )
        page_layout.add(
            Barcode(
                data="https://www.borbpdf.com",
                type=BarcodeType.QR,
                width=Decimal(100),
                height=Decimal(100),
                stroke_color=HexColor("56cbf9"),
            )
        )
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
