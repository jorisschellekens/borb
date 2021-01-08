import logging
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from ptext.functionality.export.svg_export import SVGExport
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../export/test-export-to-svg.log", level=logging.DEBUG)


class TestExportToSVG(Test):
    """
    This test attempts to export each PDF in the corpus to SVG
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../export/test-export-to-svg")

    def test_corpus(self):
        super(TestExportToSVG, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = SVGExport()
            doc = PDF.loads(pdf_file_handle, [l])
            output_file = self.output_dir / (file.stem + ".svg")
            with open(output_file, "wb") as svg_file_handle:
                svg_file_handle.write(ET.tostring(l.get_svg_per_page(0)))

        return True


if __name__ == "__main__":
    unittest.main()
