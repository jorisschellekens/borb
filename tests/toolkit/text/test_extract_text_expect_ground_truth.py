import json
import logging
import os
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from tests.test import Test
from tests.util import get_output_dir

logging.basicConfig(
    filename="../../logs/test-extract-text-expect-ground-truth.log", level=logging.DEBUG
)


class TestExtractTextExpectGroundTruth(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.global_char_abs_diff = {}
        self.number_of_wrong_chars_per_document = {}
        self.output_dir = Path(
            get_output_dir(), "test-text-extract-text-expect-ground-truth"
        )
        self.diff_file = Path(self.output_dir, "differences.json")

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203_page_0.pdf"))

    @unittest.skip
    def test_corpus(self):
        pdf_file_names = os.listdir(self.input_dir)
        pdfs = [
            (self.input_dir / x)
            for x in pdf_file_names
            if x.endswith(".pdf") and "page_0" in x
        ]
        self._test_list_of_documents(pdfs)

    def _test_document(self, file):

        if not self.output_dir.exists():
            self.output_dir.mkdir()

        txt_ground_truth_file = self.input_dir / (file.stem + ".txt")
        txt_ground_truth = ""
        with open(txt_ground_truth_file, "r") as txt_ground_truth_file_handle:
            txt_ground_truth = txt_ground_truth_file_handle.read()

        with open(file, "rb") as pdf_file_handle:
            l = SimpleTextExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            self._compare_text(file.stem, txt_ground_truth, l.get_text(0))

        # return
        return True

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
        letter_frequency_difference = {}
        for c in [k for k, v in char_count_0.items()] + [
            k for k, v in char_count_1.items()
        ]:
            f0 = char_count_0.get(c, 0)
            f1 = char_count_1.get(c, 0)
            if f0 != f1:
                letter_frequency_difference[c] = f0 - f1

        # take care of special characters
        letter_frequency_difference = self._redeem_special_characters(
            letter_frequency_difference
        )

        # update file
        if len(letter_frequency_difference) > 0:
            diff_file_data = {
                "number_of_chars_0": len(txt0),
                "number_of_chars_1": len(txt1),
                "number_of_wrong_chars": sum(
                    [abs(v) for k, v in letter_frequency_difference.items()]
                ),
                "number_of_wrong_chars_percentage": sum(
                    [abs(v) for k, v in letter_frequency_difference.items()]
                )
                / max(len(txt0), len(txt1)),
                "diffs": letter_frequency_difference,
            }
            with open(
                Path(self.output_dir, filename + ".diff.json"), "w"
            ) as json_diff_file_handle:
                json_diff_file_handle.write(json.dumps(diff_file_data, indent=3))

        # error if needed
        if len(letter_frequency_difference) > 0:
            print(
                "Character count mismatch %s : %s"
                % (filename, str(letter_frequency_difference))
            )
            raise ValueError(
                "Character count mismatch : %s" % str(letter_frequency_difference)
            )

    def _redeem_special_characters(self, differences: dict) -> dict:
        # soft hypen
        if "\xad" in differences and "-" in differences:
            k = differences["\xad"]
            differences.pop("\xad")
            differences["-"] += k
        # ligature ff
        if "ﬀ" in differences and "f" in differences:
            k = differences["ﬀ"]
            differences.pop("ﬀ")
            differences["f"] += 2 * k
        # ligature fi
        if "\ufb01" in differences and "f" in differences and "i" in differences:
            k = differences["\ufb01"]
            differences.pop("\ufb01")
            differences["f"] += k
            differences["i"] += k
        # ligature fl
        if "\ufb02" in differences and "f" in differences and "l" in differences:
            k = differences["\ufb02"]
            differences.pop("\ufb02")
            differences["f"] += k
            differences["l"] += k
        # middle dot versus bullet
        if "\u2022" in differences and "\u00b7" in differences:
            k = differences["\u2022"]
            differences.pop("\u2022")
            differences["\u00b7"] += k
        # remove zero-count items
        differences = {k: v for k, v in differences.items() if v != 0}
        # return
        return differences


if __name__ == "__main__":
    unittest.main()
