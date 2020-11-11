import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from ptext.object.canvas.listener.export.svg_export import SVGExport
from ptext.pdf import PDF
from ptext.test.base_test import BaseTest


class TestExportToSVG(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("svg")

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
            l = SVGExport()
            doc = PDF.loads(pdf_file_handle, [l])
            output_file = self.output_dir / (file.stem + ".svg")
            with open(output_file, "wb") as svg_file_handle:
                svg_file_handle.write(ET.tostring(l.get_svg(0)))


if __name__ == "__main__":
    unittest.main()
