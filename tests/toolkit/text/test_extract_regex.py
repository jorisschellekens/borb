import json
import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from tests.test import Test
from tests.util import get_output_dir

logging.basicConfig(
    filename="../../logs/test-extract-regular-expression.log", level=logging.DEBUG
)


class TestExtractRegularExpression(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-extract-regular-expression")

    @unittest.skip
    def test_corpus(self):
        super(TestExtractRegularExpression, self).test_corpus()

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def _test_document(self, file):

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
                        "text": x.text,
                        "x": int(x.get_baseline().x),
                        "y": int(x.get_baseline().y),
                        "width": int(x.get_baseline().width),
                        "height": int(x.get_baseline().height),
                    }
                    for x in l.get_matched_chunk_of_text_render_events_per_page(0)
                ]
                json_file_handle.write(json.dumps(obj, indent=4))

        return True


if __name__ == "__main__":
    unittest.main()
