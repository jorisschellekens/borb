import logging
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from ptext.action.export.svg_export import SVGExport
from ptext.action.structure.simple_structure_extraction import (
    SimpleStructureExtraction,
)
from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(filename="test_export_to_svg.log", level=logging.DEBUG)


class TestExportToSVG(BaseTest):
    """
    This test attempts to export each PDF in the corpus to SVG
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("svg")

    def test_single_document(self):
        self.input_file = self.input_dir / "0128.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = SVGExport()
            doc = PDF.loads(pdf_file_handle, [SimpleStructureExtraction(), l])
            output_file = self.output_dir / (file.stem + ".svg")
            with open(output_file, "wb") as svg_file_handle:
                svg_file_handle.write(ET.tostring(l.get_svg_per_page(0)))


if __name__ == "__main__":
    unittest.main()
