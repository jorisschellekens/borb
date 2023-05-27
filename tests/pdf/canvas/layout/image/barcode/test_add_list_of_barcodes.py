from _decimal import Decimal

from borb.pdf import Barcode
from borb.pdf import BarcodeType
from borb.pdf import Document
from borb.pdf import OrderedList
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import UnorderedList
from tests.test_case import TestCase


class TestAddListOfBarcodes(TestCase):
    def test_add_orderedlist_of_barcodes(self):

        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                test_description=f"This test creates a PDF with an OrderedList of Barcodes in it."
            )
        )
        page_layout.add(
            OrderedList()
            .add(
                Barcode(
                    data="https://www.borbpdf.com",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://www.borb-pdf.com",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://www.github.com/jorisschellekens/borb",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
        )
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_unorderedlist_of_barcodes(self):

        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                test_description=f"This test creates a PDF with an UnorderedList of Barcodes in it."
            )
        )
        page_layout.add(
            UnorderedList()
            .add(
                Barcode(
                    data="https://www.borbpdf.com",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://www.borb-pdf.com",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://www.github.com/jorisschellekens/borb",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
        )
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())
