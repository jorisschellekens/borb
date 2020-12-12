import logging
import unittest
from pathlib import Path

from ptext.action.export.markdown_export import MarkdownExport
from ptext.action.structure.simple_structure_extraction import (
    SimpleStructureExtraction,
)
from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(filename="test_export_to_markdown.py", level=logging.DEBUG)


class TestExportToMarkDown(BaseTest):
    """
    This test attempts to export each PDF in the corpus to SVG
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("markdown")

    def test_single_document(self):
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = MarkdownExport()
            doc = PDF.loads(pdf_file_handle, [SimpleStructureExtraction(), l])
            output_file = self.output_dir / (file.stem + ".md")
            with open(output_file, "w") as svg_file_handle:
                svg_file_handle.write(l.get_markdown_per_page(0))


if __name__ == "__main__":
    unittest.main()
