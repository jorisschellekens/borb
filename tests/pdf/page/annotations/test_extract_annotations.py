import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test
from tests.util import get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-extract-annotations.log"),
    level=logging.DEBUG,
)


class TestExtractAnnotations(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0066.pdf"))

    @unittest.skip
    def test_corpus(self):
        super(TestExtractAnnotations, self).test_corpus()

    def _test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            page = doc.get_page(0)

            if "Annots" in page:
                print("%s has %d annotations" % (file.stem, len(page["Annots"])))

        return True
