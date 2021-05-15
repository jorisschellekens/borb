import json
import logging
import unittest
from pathlib import Path

import typing

from ptext.pdf.document import Document

from ptext.pdf.pdf import PDF
from ptext.toolkit.structure.pdf_diff import PDFDiff
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-copy-document.log"), level=logging.DEBUG
)


class TestCopyDocument(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.input_file = Path("/home/joris/Code/pdf-corpus/0203_page_0.pdf")
        # self.input_file = Path("/home/joris/Desktop/hello_world.pdf")
        self.output_dir = Path(get_output_dir(), "test-copy-document")

    def test_copy_document(self):

        if not self.output_dir.exists():
            self.output_dir.mkdir()

        doc_a: typing.Optional[Document] = None
        with open(self.input_file, "rb") as file_handle:
            doc_a = PDF.loads(file_handle)

        with open(self.output_dir / self.input_file.name, "wb") as file_handle:
            PDF.dumps(file_handle, doc_a)

        doc_a: typing.Optional[Document] = None
        with open(self.input_file, "rb") as file_handle:
            doc_a = PDF.loads(file_handle)

        doc_b: typing.Optional[Document] = None
        with open(self.output_dir / self.input_file.name, "rb") as file_handle:
            doc_b = PDF.loads(file_handle)

        PDFDiff(doc_a, doc_b).compare()
