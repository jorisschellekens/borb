import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.list import UnorderedList
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-write-nested-unordered-list.log",
    level=logging.DEBUG,
)


class TestWriteNestedUnorderedList(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../../output/test-write-nested-unordered-list")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        ul0 = UnorderedList()
        ul0.add(Paragraph(text="Ipsum"))
        ul0.add(Paragraph(text="Dolor"))

        ul1 = UnorderedList()
        ul1.add(Paragraph(text="Ipsum"))
        ul1.add(Paragraph(text="Dolor"))
        ul1.add(Paragraph(text="Sit"))
        ul1.add(ul0)

        ul2 = UnorderedList()
        ul2.add(Paragraph(text="Lorem"))
        ul2.add(Paragraph(text="Ipsum"))
        ul2.add(Paragraph(text="Dolor"))
        ul2.add(ul1)
        ul2.layout(
            page,
            bounding_box=Rectangle(
                Decimal(100), Decimal(600), Decimal(200), Decimal(124)
            ),
        )

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
