import json
import unittest
from pathlib import Path

from borb.io.read.pdf_object import PDFObject
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestExportPDFToJSON(TestCase):
    """
    This test attempts to export each PDF in the corpus to JSON
    """

    def test_convert_pdf_to_json(self):
        input_file: Path = self.get_artifacts_directory() / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            with open(
                self.get_artifacts_directory() / "output.json", "w"
            ) as json_file_handle:
                json_file_handle.write(json.dumps(PDFObject._to_json(doc), indent=4))


if __name__ == "__main__":
    unittest.main()
