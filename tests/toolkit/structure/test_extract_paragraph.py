import logging
import unittest
from pathlib import Path
from typing import Optional

from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.pdf import PDF
from ptext.toolkit.structure.simple_paragraph_extraction import (
    SimpleParagraphExtraction,
)
from tests.test import Test

logging.basicConfig(
    filename="../../logs/test-extract-first-paragraph.log", level=logging.DEBUG
)


class TestExtractParagraph(Test):
    @unittest.skip
    def test_corpus(self):
        super(TestExtractParagraph, self).test_corpus()

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def _test_document(self, file):
        with open(file, "rb") as pdf_file_handle:

            # process document
            spe = SimpleParagraphExtraction()
            doc = PDF.loads(pdf_file_handle, [spe])

            # find longest paragraph
            biggest_paragraph: Optional[Paragraph] = None
            for p in spe.get_paragraphs(0):
                if biggest_paragraph is None or len(biggest_paragraph.text) < len(
                    p.text
                ):
                    biggest_paragraph = p

            # print
            if biggest_paragraph is not None:
                print(biggest_paragraph.text)
        return True
