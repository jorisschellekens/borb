import json
import unittest
from pathlib import Path

from ptext.object.canvas.listener.text.tf_idf_keyword_extraction import (
    TFIDFKeywordExtraction,
)
from ptext.pdf import PDF

from ptext.test.base_test import BaseTest


class TestExtractKeywords(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("keywords")

    def test_single_document(self):
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = TFIDFKeywordExtraction()
            doc = PDF.loads(pdf_file_handle, [l])

            # export txt
            output_file = self.output_dir / (file.stem + ".json")
            with open(output_file, "w") as json_file_handle:
                json_file_handle.write(
                    json.dumps([x.__dict__ for x in l.get_keywords(0, 5)], indent=4)
                )


if __name__ == "__main__":
    unittest.main()
