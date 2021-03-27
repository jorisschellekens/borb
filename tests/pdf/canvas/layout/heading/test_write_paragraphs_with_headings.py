import logging
import random
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Alignment,
    Paragraph,
    Heading,
)
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-paragraphs-with-headings.log"),
    level=logging.DEBUG,
)


class TestWriteParagraphsWithHeadings(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-paragraphs-with-headings")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        layout = MultiColumnLayout(page, number_of_columns=2)

        layout.add(Heading("The Raven", font_size=Decimal(20)))
        layout.add(
            Paragraph(
                "Edgar Allen Poe",
                font="Helvetica-Oblique",
                font_size=Decimal(8),
                font_color=X11Color("SteelBlue"),
            )
        )
        for i in range(0, 100):
            layout.add(
                Heading("Heading %d" % i, font_size=Decimal(20), outline_level=1)
            )
            for _ in range(0, random.choice([10, 20, 3])):
                layout.add(
                    Paragraph(
                        "Once upon a midnight dreary, while I pondered, weak and weary, Over many a quaint and curious volume of forgotten lore- While I nodded, nearly napping, suddenly there came a tapping, As of some one gently rapping, rapping at my chamber door. Tis some visitor, I muttered, tapping at my chamber door- Only this and nothing more.",
                        font_size=Decimal(12),
                        font_color=X11Color("SlateGray"),
                        horizontal_alignment=Alignment.LEFT,
                    )
                )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
