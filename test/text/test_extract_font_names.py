import logging

from ptext.action.text.font_extraction import FontExtraction
from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(filename="test_extract_font_names.log", level=logging.DEBUG)


class TestExtractFontNames(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_single_document(self):
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            l = FontExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for fn in l.get_font_names_per_page(0):
                print(fn)
