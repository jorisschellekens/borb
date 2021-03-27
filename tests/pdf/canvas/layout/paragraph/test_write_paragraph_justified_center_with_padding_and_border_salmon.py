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
    filename=Path(
        get_log_dir(),
        "test-write-paragraph-justified-center-with-padding-and-border-salmon.log",
    ),
    level=logging.DEBUG,
)


class TestWriteParagraphJustifiedCenterWithPaddingAndBorder(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(),
            "test-write-paragraph-justified-center-with-padding-and-border-salmon",
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

        padding = Decimal(5)
        layout_rect = Paragraph(
            "Once upon a midnight dreary,\nwhile I pondered weak and weary,\nover many a quaint and curious\nvolume of forgotten lore",
            font_size=Decimal(20),
            horizontal_alignment=Alignment.CENTERED,
            text_alignment=Alignment.CENTERED,
            respect_newlines_in_text=True,
            padding_top=padding,
            padding_right=padding,
            padding_bottom=padding,
            padding_left=padding,
            border_right=True,
            border_top=True,
            border_color=X11Color("Green"),
            font_color=X11Color("Salmon"),
        ).layout(
            page,
            Rectangle(Decimal(20), Decimal(600), Decimal(500), Decimal(124)),
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
