import json
import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.color.color_spectrum_extraction import (
    ColorSpectrumExtraction,
)
from tests.test import Test
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-extract-colors.log"), level=logging.DEBUG
)


class TestExtractColors(Test):
    """
    This test attempts to extract the colors for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_file = Path(get_output_dir(), "test-extract-colors/output.json")

    @unittest.skip
    def test_corpus(self):
        super(TestExtractColors, self).test_corpus()

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203_page_0.pdf"))

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_file.parent.exists():
            self.output_file.parent.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = ColorSpectrumExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            colors = []
            for t in l.get_colors_per_page(0, limit=16):
                colors.append(
                    {
                        "red": float(t[0].red),
                        "green": float(t[0].green),
                        "blue": float(t[0].blue),
                        "count": int(t[1]),
                    }
                )

            # write output
            with open(self.output_file, "w") as json_file_handle:
                json_file_handle.write(json.dumps(colors))

        return True


if __name__ == "__main__":
    unittest.main()
