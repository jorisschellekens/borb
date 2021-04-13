import json
import logging
import unittest
from pathlib import Path

from ptext.pdf.canvas.color.color import RGBColor

from ptext.pdf.canvas.layout.image import Image

from ptext.pdf.document import Document

from ptext.pdf.pdf import PDF
from ptext.toolkit.export.json_to_pdf import JSONToPDF
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-export-json-to-pdf.log"), level=logging.DEBUG
)


class TestExportJSONToPDF(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-export-json-to-pdf")

    def test(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        for file_to_convert in [
            "example-json-input-001.json",
            "example-json-input-002.json",
            "example-json-input-003.json",
        ]:

            json_data = None
            path_to_json = Path(__file__).parent / file_to_convert
            with open(path_to_json, "r") as json_file_handle:
                json_data = json.loads(json_file_handle.read())

            # convert
            document: Document = JSONToPDF.convert_json_to_pdf(json_data)

            # store
            output_file = self.output_dir / (file_to_convert + ".pdf")
            with open(output_file, "wb") as pdf_file_handle:
                PDF.dumps(pdf_file_handle, document)

        return True


if __name__ == "__main__":
    unittest.main()
