import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from tests.test import Test

logging.basicConfig(filename="../text/test-extract-text.log", level=logging.DEBUG)


class TestExtractText(Test):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../text/test-extract-text")

    def test_corpus(self):
        super(TestExtractText, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = SimpleTextExtraction()
            doc = PDF.loads(pdf_file_handle, [l])

            # export txt
            output_file = self.output_dir / (file.stem + ".txt")
            with open(output_file, "w") as txt_file_handle:
                txt_file_handle.write(l.get_text(0))

        return True


if __name__ == "__main__":
    unittest.main()
