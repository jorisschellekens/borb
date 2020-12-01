import unittest

from ptext.object.canvas.listener.color.color_spectrum_extraction import (
    ColorSpectrumExtraction,
)
from ptext.pdf import PDF
from ptext.test.base_test import BaseTest


class TestExtractColors(BaseTest):
    """
    This test attempts to extract the colors for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_single_document(self):
        self.input_file = self.input_dir / "document_556_single_page.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        with open(file, "rb") as pdf_file_handle:
            l = ColorSpectrumExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for t in l.get_colors_per_page(0, limit=16):
                print("rgb(%d, %d, %d) : %d" % (t[0].red, t[0].green, t[0].blue, t[1]))


if __name__ == "__main__":
    unittest.main()
