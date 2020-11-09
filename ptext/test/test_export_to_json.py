import json
import unittest
from pathlib import Path

from ptext.object.canvas.listener.export.svg_export import SVGExport
from ptext.pdf import PDF
import xml.etree.ElementTree as ET

from ptext.test.base_test import BaseTest


class TestExportToJSON(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("json")

    def test_single_document(self):
        self.input_file = self.input_dir / "document_955_single_page.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            output_file = self.output_dir / (file.stem + ".json")

            # export to json
            with open(output_file, "w") as json_file_handle:
                json_file_handle.write(json.dumps(doc.as_dict(), indent=4))


if __name__ == "__main__":
    unittest.main()
