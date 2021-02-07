import json
import logging
import unittest
from pathlib import Path

from ptext.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../text/test-extract-regular-expression.log", level=logging.DEBUG
)


class TestExtractRegularExpression(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../text/test-extract-regular-expression")

    def test_corpus(self):
        super(TestExtractRegularExpression, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = RegularExpressionTextExtraction("[sS]orbitol")
            doc = PDF.loads(pdf_file_handle, [l])

            # export matches
            output_file = self.output_dir / (file.stem + ".json")
            with open(output_file, "w") as json_file_handle:
                obj = [
                    {
                        "text": x.get_text(),
                        "x0": int(x.get_baseline().x0),
                        "y0": int(x.get_baseline().y0),
                        "x1": int(x.get_baseline().x1),
                        "y1": int(x.get_baseline().y1),
                    }
                    for x in l.get_matched_text_render_info_events_per_page(0)
                ]
                json_file_handle.write(json.dumps(obj, indent=4))

        return True


if __name__ == "__main__":
    unittest.main()
