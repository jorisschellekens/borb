import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.export.jpg_export import JPGExport
from tests.test import Test
from tests.util import get_output_dir

logging.basicConfig(filename="../../logs/test-export-to-jpg.log", level=logging.DEBUG)


class TestExportToSVG(Test):
    """
    This test attempts to export each PDF in the corpus to SVG
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-export-to-jpg")

    @unittest.skip
    def test_corpus(self):
        super(TestExportToSVG, self).test_corpus()

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = JPGExport()
            doc = PDF.loads(pdf_file_handle, [l])
            output_file = self.output_dir / (file.stem + ".jpg")
            with open(output_file, "wb") as svg_file_handle:
                im = l.image_per_page.get(0)
                im.save(output_file)

        return True


if __name__ == "__main__":
    unittest.main()
