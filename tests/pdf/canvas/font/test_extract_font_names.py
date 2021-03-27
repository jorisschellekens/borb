import json
import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.text.font_extraction import FontExtraction
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-extract-font-names.log"), level=logging.DEBUG
)


class TestExtractFontNames(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_file = Path(get_output_dir(), "test-extract-font-names/output.json")
        self.input_file = Path("/home/joris/Code/pdf-corpus/0066.pdf")

    def test_extract_font_names(self):

        # create output directory if it does not exist yet
        if not self.output_file.parent.exists():
            self.output_file.parent.mkdir()

        # extract font names
        font_names = []
        with open(self.input_file, "rb") as pdf_file_handle:
            l = FontExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for fn in l.get_font_names_per_page(0):
                font_names.append(str(fn))

        # write output
        with open(self.output_file, "w") as json_file_handle:
            json_file_handle.write(json.dumps(font_names))

        return True
