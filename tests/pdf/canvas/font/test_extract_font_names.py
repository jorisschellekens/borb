import logging
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.text.font_extraction import FontExtraction
from tests.test import Test

logging.basicConfig(
    filename="../../../logs/test-extract-font-names.log", level=logging.DEBUG
)


class TestExtractFontNames(Test):
    def test_corpus(self):
        super(TestExtractFontNames, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0066.pdf"))

    def test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            l = FontExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for fn in l.get_font_names_per_page(0):
                print(fn)
        return True
