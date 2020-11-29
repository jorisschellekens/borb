import unittest
from pathlib import Path

from ptext.object.canvas.listener.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from ptext.pdf import PDF
from ptext.test.base_test import BaseTest


class TestExtractTextMarkNonAscii(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("non_ascii_txt")

    def test_single_document(self):
        self.input_file = self.input_dir / "document_652.pdf"
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

            p = self._non_ascii_percentage(l.get_text(0))

            if p > 0.01:

                # export txt
                output_file = self.output_dir / (file.stem + ".txt")
                with open(output_file, "w") as txt_file_handle:
                    txt_file_handle.write(l.get_text(0))

                raise ValueError("PDF with more than 1% non-ascii characters")

    def _non_ascii_percentage(self, txt: str) -> float:
        m = len(txt)
        if m == 0:
            return 0
        n = 0
        for c in txt:
            if (
                c
                not in "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 ,.?!;: -_ (){}[] '\" \n\t\r /+*$#@"
            ):
                n += 1
        return n / m


if __name__ == "__main__":
    unittest.main()
