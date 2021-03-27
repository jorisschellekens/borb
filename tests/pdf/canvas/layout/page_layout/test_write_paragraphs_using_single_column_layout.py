import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
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
        get_log_dir(), "test-write-paragraphs-using-single-column-layout.log"
    ),
    level=logging.DEBUG,
)


class TestWriteParagraphsUsingSingleColumnLayout(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-write-paragraphs-using-single-column-layout"
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

        layout = SingleColumnLayout(page)

        layout.add(
            Paragraph(
                "Once upon a midnight dreary, while I pondered weak and weary, over many a quaint and curious volume of forgotten lore.",
                font_size=Decimal(20),
                text_alignment=Alignment.RIGHT,
                horizontal_alignment=Alignment.RIGHT,
            )
        )
        layout.add(
            Paragraph(
                "While I nodded, nearly napping, suddenly there came a tapping. As of someone gently rapping, rapping at my chamberdoor.",
                font_size=Decimal(20),
                text_alignment=Alignment.RIGHT,
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
