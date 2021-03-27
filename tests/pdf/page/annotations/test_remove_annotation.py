import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-remove-annotations.log"),
    level=logging.DEBUG,
)


class TestRemoveAnnotation(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-remove-annotation")

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0200.pdf"))

    @unittest.skip
    def test_corpus(self):
        super(TestRemoveAnnotation, self).test_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        doc = None
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # remove first annotation
        if "Annots" in doc.get_page(0):
            annots = doc.get_page(0)["Annots"]
            annots[0]["P"] = None
            doc.get_page(0)["Annots"] = annots[1:0]
            pass

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)
        return True
