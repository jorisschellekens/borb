import logging
import time
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../../logs/test-copy-document.log", level=logging.DEBUG)


class TestCopyDocument(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../output/test-copy-document")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0041.pdf"))

    def test_corpus(self):
        super(TestCopyDocument, self).test_corpus()

    def test_previous_fails(self):
        self.maximum_test_time = 60
        super(TestCopyDocument, self).test_previous_fails()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        # attempt to read PDF
        delta = time.time()
        doc = None
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)
        print("time elapsed : %d" % (time.time() - delta))
        delta = time.time()

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)
        print("time elapsed : %d" % (time.time() - delta))
        delta = time.time()

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)
        print("time elapsed : %d" % (time.time() - delta))
        delta = time.time()

        return True
