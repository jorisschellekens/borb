import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test
from tests.util import get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-extract-embedded-files.log"), level=logging.DEBUG
)


class TestExtractEmbeddedFiles(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0164.pdf"))

    @unittest.skip
    def test_corpus(self):
        super(TestExtractEmbeddedFiles, self).test_corpus()

    def _test_document(self, file):
        doc = None
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # extract all embedded files
        embedded_files = doc.get_embedded_files()

        # assert(s)
        assert len(embedded_files) == 1
