import logging
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../embedded_files/test-get-embedded-files.log", level=logging.DEBUG
)


class TestGetEmbeddedFiles(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0164.pdf"))

    def test_corpus(self):
        super(TestGetEmbeddedFiles, self).test_corpus()

    def test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

            if (
                "Names" in doc["XRef"]["Trailer"]["Root"]
                and "EmbeddedFiles" in doc["XRef"]["Trailer"]["Root"]["Names"]
            ):
                print("%s has embedded files" % file.stem)

        return True
