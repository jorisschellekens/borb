import logging
import unittest
from pathlib import Path


from ptext.pdf.canvas.layout.barcode import BarcodeType, Barcode

from ptext.pdf.canvas.color.color import HexColor

from ptext.pdf.canvas.font.simple_font.font_type_3 import Type3Font
from ptext.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout, PageLayout

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import ChunkOfText, Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-with-external-font.log"),
    level=logging.DEBUG,
)


class TestWriteWithExternalFont(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-with-external-font")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # path to font
        font_path: Path = Path(__file__).parent / "Jsfont-Regular.ttf"
        assert font_path.exists()

        # layout
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            Paragraph(
                "Hello World,",
                font=TrueTypeFont.true_type_font_from_file(font_path),
                font_size=Decimal(40),
                font_color=HexColor("FFCC00"),
            )
        )

        layout.add(
            Paragraph(
                """
                pText can now write in any custom TTF font. Like this one, which is a stylized copy of my handwriting. 
                Of course, you could also pick a more sensible font. Like Comic Sans, Roboto, Open Sans, and many others.
                In fact, pText can use any TTF font. 
                """,
                font=TrueTypeFont.true_type_font_from_file(font_path),
                font_size=Decimal(20),
                font_color=HexColor("646E78"),
            )
        )

        layout.add(
            Paragraph(
                """
                Finally, you have the option to match your own custom style and brand.
                For more examples, check out GitHub. Don't forget to star the repo :-)
                """,
                font=TrueTypeFont.true_type_font_from_file(font_path),
                font_size=Decimal(20),
                font_color=HexColor("68C3D4"),
            )
        )

        layout.add(
            Barcode(
                data="https://github.com/jorisschellekens/ptext-release",
                type=BarcodeType.QR,
                width=Decimal(64),
                height=Decimal(64),
                stroke_color=HexColor("FFCC00"),
            )
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
