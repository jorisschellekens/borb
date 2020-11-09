import json
import unittest
from pathlib import Path

from ptext.object.canvas.listener.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from ptext.object.canvas.listener.text.simple_text_extraction import (
    SimpleTextExtraction,
)
from ptext.object.canvas.listener.text.tf_idf_keyword_extraction import (
    TFIDFKeywordExtraction,
)
from ptext.pdf import PDF

from ptext.test.base_test import BaseTest


class TestExtractRegularExpression(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("regex")

    def test_single_document(self):
        self.input_file = self.input_dir / "document_1031.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = RegularExpressionTextExtraction("[hH]ealth")
            doc = PDF.loads(pdf_file_handle, [l])

            # export matches
            output_file = self.output_dir / (file.stem + ".json")
            with open(output_file, "w") as json_file_handle:
                obj = [
                    {
                        "text": x.get_text(),
                        "x0": x.get_baseline().x0,
                        "y0": x.get_baseline().y0,
                        "x1": x.get_baseline().x1,
                        "y1": x.get_baseline().y1,
                    }
                    for x in l.get_matched_text_render_info_events_per_page(0)
                ]
                json_file_handle.write(json.dumps(obj, indent=4))


if __name__ == "__main__":
    unittest.main()
