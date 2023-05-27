from _decimal import Decimal

from borb.pdf import Barcode
from borb.pdf import BarcodeType
from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from tests.test_case import TestCase


class TestAddBarcode(TestCase):
    def _test_add_barcode_using_type(
        self, data: str, barcode_type: BarcodeType
    ) -> Document:
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                test_description=f"This test creates a PDF with a Barcode of type {barcode_type.name} in it."
            )
        )
        page_layout.add(
            Barcode(
                data=data, type=barcode_type, width=Decimal(100), height=Decimal(100)
            )
        )
        return pdf

    def test_add_barcode_using_type_code_128(self):
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="12345678", barcode_type=BarcodeType.CODE_128
                ),
            )
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_barcode_using_type_code_39(self):
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="12345678", barcode_type=BarcodeType.CODE_39
                ),
            )
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_barcode_using_type_ean(self):
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="123456789910", barcode_type=BarcodeType.EAN
                ),
            )
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_barcode_using_type_ean_13(self):
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="123456789101", barcode_type=BarcodeType.EAN_13
                ),
            )
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_barcode_using_type_ean_14(self):
        with open(self.get_fifth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="1234567891011", barcode_type=BarcodeType.EAN_14
                ),
            )
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_barcode_using_type_ean_8(self):
        with open(self.get_sixth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="1234567891011", barcode_type=BarcodeType.EAN_8
                ),
            )
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_barcode_using_type_gs_128(self):
        with open(self.get_seventh_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="1234567891011", barcode_type=BarcodeType.GS_128
                ),
            )
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_add_barcode_using_type_isbn_10(self):
        with open(self.get_eight_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="1234567891011", barcode_type=BarcodeType.ISBN_10
                ),
            )
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())

    def test_add_barcode_using_type_isbn_13(self):
        with open(self.get_nineth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(
                pdf_file_handle,
                self._test_add_barcode_using_type(
                    data="9781234567891011", barcode_type=BarcodeType.ISBN_13
                ),
            )
        self.compare_visually_to_ground_truth(self.get_nineth_output_file())
        self.check_pdf_using_validator(self.get_nineth_output_file())
