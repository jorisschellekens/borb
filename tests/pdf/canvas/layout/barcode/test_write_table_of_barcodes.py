import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-table-of-barcodes.log"),
    level=logging.DEBUG,
)


class TestWriteTableOfBarcodes(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-table-of-barcodes")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # set layout
        layout = SingleColumnLayout(page)

        # add barcode
        layout.add(
            Table(number_of_rows=5, number_of_columns=2)
            .add(Paragraph("CODE 128"))
            .add(
                Barcode(
                    data="123456789128",
                    type=BarcodeType.CODE_128,
                    width=Decimal(128),
                    stroke_color=HexColor("#080708"),
                )
            )
            .add(Paragraph("CODE 39"))
            .add(
                Barcode(
                    data="123456789128",
                    type=BarcodeType.CODE_39,
                    width=Decimal(128),
                    stroke_color=HexColor("#3772FF"),
                )
            )
            .add(Paragraph("EAN 13"))
            .add(
                Barcode(
                    data="123456789128",
                    type=BarcodeType.EAN_13,
                    width=Decimal(128),
                    stroke_color=HexColor("#DF2935"),
                )
            )
            .add(Paragraph("EAN 14"))
            .add(
                Barcode(
                    data="1234567891280",
                    type=BarcodeType.EAN_14,
                    width=Decimal(128),
                    stroke_color=HexColor("#FDCA40"),
                )
            )
            .add(Paragraph("QR"))
            .add(
                Barcode(
                    data="1234567891280",
                    type=BarcodeType.QR,
                    width=Decimal(128),
                    stroke_color=HexColor("#E6E8E6"),
                    fill_color=HexColor("#DF2935"),
                )
            )
            .set_padding_on_all_cells(Decimal(10), Decimal(5), Decimal(5), Decimal(5))
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
