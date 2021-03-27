import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import LineOfText, Alignment
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-line-of-text-justified-right.log"),
    level=logging.DEBUG,
)


class TestWriteLineOfTextJustifiedRight(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-write-line-of-text-justified-right"
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

        for i, s in enumerate(
            [
                "Once upon a midnight dreary,",
                "while I pondered weak and weary,",
                "over many a quaint and curious",
                "volume of forgotten lore",
            ]
        ):
            LineOfText(
                s,
                font_size=Decimal(20),
                horizontal_alignment=Alignment.RIGHT,
            ).layout(
                page,
                Rectangle(
                    Decimal(20), Decimal(724 - 24 * i), Decimal(500), Decimal(24)
                ),
            )

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=X11Color("Salmon"),
            rectangle=Rectangle(
                Decimal(20), Decimal(724 - 24 * 3), Decimal(500), Decimal(24 * 4)
            ),
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
