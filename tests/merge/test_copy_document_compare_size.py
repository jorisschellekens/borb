import logging
import time
import typing
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../merge/test-copy-document-compare-size.log", level=logging.DEBUG
)


class TestCopyDocumentCompareSize(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.size_tuples: typing.Dictionary[str, typing.Tuple[int, int]] = {}
        self.output_dir = Path("../merge/test-copy-document-compare-size")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0474.pdf"))

    def test_corpus(self):
        super(TestCopyDocumentCompareSize, self).test_corpus()

    def test_previous_fails(self):
        self.maximum_test_time = 60
        super(TestCopyDocumentCompareSize, self).test_previous_fails()

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

        size_of_original = Path(file).stat().st_size
        size_of_copy = Path(out_file).stat().st_size
        ratio = (size_of_copy + 0.0) / size_of_original
        print("%s %d %d %f" % (file.stem, size_of_original, size_of_copy, ratio))

        if ratio > 1.05:
            raise Exception("Copied PDF is %f times larger than the original" % ratio)

        return True
