import logging

from ptext.functionality.text.font_extraction import FontExtraction
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../font/test-extract-font-names.log", level=logging.DEBUG)


class TestExtractFontNames(Test):
    def test_corpus(self):
        super(TestExtractFontNames, self).test_corpus()

    def test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            l = FontExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for fn in l.get_font_names_per_page(0):
                print(fn)
        return True
