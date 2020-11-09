import unittest
from pathlib import Path

from ptext.object.canvas.listener.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from ptext.object.canvas.listener.text.tf_idf_keyword_extraction import (
    TFIDFKeywordExtraction,
)
from ptext.pdf import PDF

from ptext.test.base_test import BaseTest


class TestExtractText(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("txt")

    def test_single_document(self):
        self.input_file = self.input_dir / "document_37.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

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


if __name__ == "__main__":
    unittest.main()
