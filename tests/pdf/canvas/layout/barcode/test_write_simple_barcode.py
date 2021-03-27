import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-simple-barcode.log"), level=logging.DEBUG
)


class TestWriteSimpleBarcode(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-simple-barcode")

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
            Barcode(
                data="123456789128",
                type=BarcodeType.CODE_128,
                width=Decimal(128),
                stroke_color=HexColor("#080708"),
            )
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
