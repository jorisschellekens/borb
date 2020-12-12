import logging

from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(filename="test_extract_low_level_author.log", level=logging.DEBUG)


class TestExtractLowLevelAuthor(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_single_document(self):
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            author = doc["XRef"]["Trailer"]["Info"]["Author"]
            print("The author of this PDF is %s" % author)
