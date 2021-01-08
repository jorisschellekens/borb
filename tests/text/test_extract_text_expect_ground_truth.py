import logging
import unittest

from ptext.functionality.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../text/test-extract-text-expect-ground-truth.log", level=logging.DEBUG
)


class TestExtractTextExpectGroundTruth(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.global_char_abs_diff = {}
        self.number_of_wrong_chars_per_document = {}

    def test_document(self, file):

        if "page_0" not in file.stem:
            return

        txt_ground_truth_file = self.input_dir / (file.stem + ".txt")
        txt_ground_truth = ""
        with open(txt_ground_truth_file, "r") as txt_ground_truth_file_handle:
            txt_ground_truth = txt_ground_truth_file_handle.read()

        with open(file, "rb") as pdf_file_handle:
            l = SimpleTextExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            self._compare_text(file.stem, txt_ground_truth, l.get_text(0))

    def _compare_text(self, filename: str, txt0: str, txt1: str):
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

        # count difference in frequency
        diffs = {}
        for c in [k for k, v in char_count_0.items()] + [
            k for k, v in char_count_1.items()
        ]:
            f0 = char_count_0.get(c, 0)
            f1 = char_count_1.get(c, 0)
            if f0 != f1:
                diffs[c] = f0 - f1

        # take care of special characters
        diffs = self._redeem_special_characters(diffs)

        # update count per character
        for c in diffs:
            if c not in self.global_char_abs_diff:
                self.global_char_abs_diff[c] = 0
            self.global_char_abs_diff[c] += diffs[c]

        # update count per document
        self.number_of_wrong_chars_per_document[filename] = sum(
            [abs(v) for k, v in diffs.items()]
        )

        # error if needed
        if len(diffs) > 0:
            raise ValueError("Character count mismatch : %s" % str(diffs))

    def _redeem_special_characters(self, differences: dict) -> dict:
        # ligature ff
        if "ﬀ" in differences and "f" in differences:
            k = differences["ﬀ"]
            differences.pop("ﬀ")
            differences["f"] -= 2 * k
        # ligature fi
        if "\ufb01" in differences and "f" in differences and "i" in differences:
            k = differences["\ufb01"]
            differences.pop("\ufb01")
            differences["f"] -= k
            differences["i"] -= k
        # ligature fl
        if "\ufb02" in differences and "f" in differences and "l" in differences:
            k = differences["\ufb02"]
            differences.pop("\ufb02")
            differences["f"] -= k
            differences["l"] -= k
        # remove zero-count items
        differences = {k: v for k, v in differences.items() if v != 0}
        # return
        return differences

    def _test_info_as_json(self):
        json = super(TestExtractTextExpectGroundTruth, self)._test_info_as_json()
        N = sum([v for k, v in self.global_char_abs_diff.items()])
        if N == 0:
            return json
        else:
            json["messed_up_chars"] = {
                k: v for k, v in self.global_char_abs_diff.items() if v / N > 0.01
            }
            json[
                "number_of_wrong_chars_per_document"
            ] = self.number_of_wrong_chars_per_document
        return json


if __name__ == "__main__":
    unittest.main()
