from _decimal import Decimal

from borb.pdf import Barcode
from borb.pdf import BarcodeType
from borb.pdf import Document
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from tests.test_case import TestCase


class TestAddTableOfBarcodes(TestCase):
    def test_add_table_of_barcodes(self):

        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.add(
            self.get_test_header(
                test_description=f"This test creates a PDF with an FlexibleColumnWidthTable of Barcodes in it."
            )
        )
        page_layout.add(
            FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3)
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
            # 2nd row
            .add(
                Barcode(
                    data="https://pypi.org/project/borb/",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://www.linkedin.com/company/75661242/",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://www.kaggle.com/general/270810",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            # 3rd row
            .add(
                Barcode(
                    data="https://stackoverflow.com/questions/tagged/borb",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://stackabuse.com/author/jorisschellekens/",
                    type=BarcodeType.QR,
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Barcode(
                    data="https://www.borbpdf.com",
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
