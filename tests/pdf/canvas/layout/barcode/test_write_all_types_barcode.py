import unittest
from datetime import datetime
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


class TestWriteSimpleBarcode(unittest.TestCase):
    """
    This test creates a PDF with a barcode for each value in the BarcodeType enum.
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_write_document(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # set layout
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a barcode for each value in the BarcodeType enum."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add barcode
        for i, t in enumerate(BarcodeType):
            data = "1234567891280"
            if t == BarcodeType.ISBN:
                data = "9781234567891280"
            if (
                t == BarcodeType.EAN
                or t == BarcodeType.EAN_8
                or t == BarcodeType.EAN_13
                or t == BarcodeType.EAN_14
            ):
                data = "4509781234567891"
            if t == BarcodeType.JAN:
                data = "4509781234567891"
            if i % 5 == 0:
                page = Page()
                pdf.append_page(page)
                layout = SingleColumnLayout(page)
            layout.add(
                Barcode(
                    data=data,
                    type=t,
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
