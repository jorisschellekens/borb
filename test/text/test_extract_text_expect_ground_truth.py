import logging
import unittest

from ptext.action.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(
    filename="../test_extract_text_expect_ground_truth.log", level=logging.DEBUG
)


class TestExtractTextExpectGroundTruth(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.messed_up_characters = {}

    def test_single_document(self):
        self.input_file = self.input_dir / "0246_page_0.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        if "page_0" not in file.stem:
            return

        txt_ground_truth_file = self.input_dir / (file.stem + ".txt")
        txt_ground_truth = ""
        with open(txt_ground_truth_file, "r") as txt_ground_truth_file_handle:
            txt_ground_truth = txt_ground_truth_file_handle.read()

        with open(file, "rb") as pdf_file_handle:
            l = SimpleTextExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            self._compare_text(txt_ground_truth, l.get_text(0))

    def _compare_text(self, txt0: str, txt1: str):
        char_count_0 = {}
        for c in txt0:
            if c not in char_count_0:
                char_count_0[c] = 1
            else:
                char_count_0[c] += 1
        char_count_1 = {}
        for c in txt1:
            if c not in char_count_1:
                char_count_1[c] = 1
            else:
                char_count_1[c] += 1
        for c in "\t\n\r \xa0":
            char_count_0[c] = 0
            char_count_1[c] = 0
        diffs = {}
        for c in [k for k, v in char_count_0.items()] + [
            k for k, v in char_count_1.items()
        ]:
            f0 = char_count_0.get(c, 0)
            f1 = char_count_1.get(c, 0)
            if f0 != f1:
                diffs[c] = f0 - f1
            if c not in self.messed_up_characters:
                self.messed_up_characters[c] = 0
            self.messed_up_characters[c] += abs(f0 - f1)
        if len(diffs) > 0:
            raise ValueError("Character count mismatch : %s" % str(diffs))

    def _test_info_as_json(self):
        json = super(TestExtractTextExpectGroundTruth, self)._test_info_as_json()
        N = sum([v for k, v in self.messed_up_characters.items()])
        if N == 0:
            return json
        else:
            json["messed_up_chars"] = {
                k: v for k, v in self.messed_up_characters.items() if v / N > 0.01
            }
        return json


if __name__ == "__main__":
    unittest.main()
