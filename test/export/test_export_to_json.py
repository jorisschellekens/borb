import json
import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(filename="test_export_to_json.log", level=logging.DEBUG)


class TestExportToJSON(BaseTest):
    """
    This test attempts to export each PDF in the corpus to JSON
    """

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
                json_file_handle.write(
                    json.dumps(doc.to_json_serializable(doc), indent=4)
                )


if __name__ == "__main__":
    unittest.main()
