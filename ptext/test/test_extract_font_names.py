import json
import unittest
from pathlib import Path

from ptext.object.canvas.listener.text.font_name_extraction import FontExtraction
from ptext.object.canvas.listener.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from ptext.pdf import PDF
from ptext.test.base_test import BaseTest


class TestExtractFontNames(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_single_document(self):
        self.input_file = self.input_dir / "document_1031.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            l = FontExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for fn in l.get_font_names_per_page(0):
                print(fn)
