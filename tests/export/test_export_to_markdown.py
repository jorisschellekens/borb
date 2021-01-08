import logging
import unittest
from pathlib import Path

from ptext.functionality.export.markdown_export import MarkdownExport
from ptext.functionality.structure.simple_structure_extraction import (
    SimpleStructureExtraction,
)
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../export/test-export-to-markdown.log", level=logging.DEBUG
)


class TestExportToMarkDown(Test):
    """
    This test attempts to export each PDF in the corpus to SVG
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../export/test-export-to-markdown")

    def test_corpus(self):
        super(TestExportToMarkDown, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = MarkdownExport()
            doc = PDF.loads(pdf_file_handle, [SimpleStructureExtraction(), l])
            output_file = self.output_dir / (file.stem + ".md")
            with open(output_file, "w") as svg_file_handle:
                svg_file_handle.write(l.get_markdown_per_page(0))

        return True


if __name__ == "__main__":
    unittest.main()
