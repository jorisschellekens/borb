import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


class TestReadBrokenXRef(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def _read_broken_xref_001(self):

        # attempt to read PDF
        input_file_001 = Path(__file__).parent / "input_001.pdf"
        doc_001 = None
        with open(input_file_001, "rb") as in_file_handle:
            doc_001 = PDF.loads(in_file_handle)

    def test_read_broken_xref_001(self):
        self.assertRaises(AssertionError, self._read_broken_xref_001)

    def _read_broken_xref_002(self):

        # attempt to read PDF
        input_file_001 = Path(__file__).parent / "input_002.pdf"
        doc_001 = None
        with open(input_file_001, "rb") as in_file_handle:
            doc_001 = PDF.loads(in_file_handle)

    def test_read_broken_xref_002(self):
        self.assertRaises(AssertionError, self._read_broken_xref_002)
