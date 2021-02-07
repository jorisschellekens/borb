import unittest
import zlib
from pathlib import Path

from ptext.io.read.types import Stream, Decimal, Name, Dictionary
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import ChunkOfText
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class TestWriteHelloWorld(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../write/test-write-hello-world-easier")

    def test_write_hello_world(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        ChunkOfText(
            "Koksu jeden gram", font_size=Decimal(24), color=X11Color("YellowGreen")
        ).layout(
            page, Rectangle(Decimal(100), Decimal(724), Decimal(100), Decimal(100))
        )

        # determine output location
        out_file = self.output_dir / ("hello_world_out.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
