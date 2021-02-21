import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import (
    Justification,
    Paragraph,
)
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-write-paragraph-justified-center-with-padding.log",
    level=logging.DEBUG,
)


class TestWriteParagraphJustifiedCenterWithPadding(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            "../../../../output/test-write-paragraph-justified-center-with-padding"
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
            font_color=X11Color("YellowGreen"),
            justification=Justification.CENTERED,
            respect_newlines_in_text=True,
            padding_top=padding,
            padding_right=padding,
            padding_bottom=padding,
            padding_left=padding,
        ).layout(
            page,
            Rectangle(Decimal(20), Decimal(600), Decimal(500), Decimal(124)),
        )

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=X11Color("Red"), rectangle=layout_rect
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
