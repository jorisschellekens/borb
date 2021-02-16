import logging
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../../logs/test-read-info-dictionary-author.log", level=logging.DEBUG
)


class TestReadInfoDictionaryAuthor(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0328_page_0.pdf"))

    def test_corpus(self):
        super(TestReadInfoDictionaryAuthor, self).test_corpus()

    def test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            if "XRef" not in doc:
                return False
            if "Trailer" not in doc["XRef"]:
                return False
            if (
                "Info" in doc["XRef"]["Trailer"]
                and "Author" in doc["XRef"]["Trailer"]["Info"]
            ):
                author = doc["XRef"]["Trailer"]["Info"]["Author"]
                print("The author of this PDF is %s" % author)
        return True
