import logging
import unittest
from pathlib import Path

from ptext.functionality.color.color_spectrum_extraction import (
    ColorSpectrumExtraction,
)
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../color/test-extract-colors.log", level=logging.DEBUG)


class TestExtractColors(Test):
    """
    This test attempts to extract the colors for each PDF in the corpus
    """

    def test_corpus(self):
        super(TestExtractColors, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0066.pdf"))

    def test_document(self, file):

        with open(file, "rb") as pdf_file_handle:
            l = ColorSpectrumExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for t in l.get_colors_per_page(0, limit=16):
                print("rgb(%d, %d, %d) : %d" % (t[0].red, t[0].green, t[0].blue, t[1]))

        return True


if __name__ == "__main__":
    unittest.main()
