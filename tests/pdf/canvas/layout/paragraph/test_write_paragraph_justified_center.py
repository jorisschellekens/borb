import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import (
    Alignment,
    Paragraph,
)
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-paragraph-justified-center.log"),
    level=logging.DEBUG,
)


class TestWriteParagraphJustifiedCenter(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-write-paragraph-justified-center"
        )

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        Paragraph(
            "Once upon a midnight dreary, while I pondered weak and weary, over many a quaint and curious volume of forgotten lore",
            font_size=Decimal(20),
            text_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
        ).layout(
            page,
            Rectangle(Decimal(20), Decimal(600), Decimal(500), Decimal(124)),
        )

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=X11Color("Red"),
            rectangle=Rectangle(Decimal(20), Decimal(600), Decimal(500), Decimal(124)),
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
