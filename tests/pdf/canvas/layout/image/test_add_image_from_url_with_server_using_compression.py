import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import HexColor
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.pdf import PDF

from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import Image

from decimal import Decimal


class TestAddImageFromURLWithServerUsingCompression(unittest.TestCase):
    """
    This test creates a PDF with a (PNG) Image in it, this is specified by a URL
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


    def test_add_image_by_url(self):

        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Image in it, this is specified by a URL. "
                    "The server uses compression. This would previously fail with an UnidentifiedImageError"
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add Image
        url = "https://d262ijfj3ea8g5.cloudfront.net/2017/img/logo.png"  # content_encoding 'gzip' or 'deflate' used here
        layout.add(Image(url,
                         width=Decimal(32),
                         height=Decimal(32)))

        # store
        with open(self.output_dir / "output.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)


if __name__ == "__main__":
    unittest.main()
