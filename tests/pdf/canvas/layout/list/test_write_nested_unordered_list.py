import logging
import unittest
from pathlib import Path

from ptext.pdf.canvas.layout.list import UnorderedList
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-nested-unordered-list.log"),
    level=logging.DEBUG,
)


class TestWriteNestedUnorderedList(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-nested-unordered-list")

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

        layout = SingleColumnLayout(page)
        layout.add(ul2)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
