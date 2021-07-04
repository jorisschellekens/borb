import unittest
from pathlib import Path

from ptext.pdf.document import Document
from ptext.pdf.pdf import PDF
from ptext.toolkit.export.html_to_pdf.html_to_pdf import HTMLToPDF
from ptext.toolkit.export.pdf_to_html import PDFToHTML


class TestExportPDFToHTML(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_example_000(self):
        self._test_convert_document("example-html-input-000.html")

    def test_example_001(self):
        self._test_convert_document("example-html-input-001.html")

    def test_example_002(self):
        self._test_convert_document("example-html-input-002.html")

    def test_example_003(self):
        self._test_convert_document("example-html-input-003.html")

    def test_example_004(self):
        self._test_convert_document("example-html-input-004.html")

    def test_example_005(self):
        self._test_convert_document("example-html-input-005.html")

    def test_example_006(self):
        self._test_convert_document("example-html-input-006.html")

    def test_example_007(self):
        self._test_convert_document("example-html-input-007.html")

    def test_example_008(self):
        self._test_convert_document("example-html-input-008.html")

    def test_example_009(self):
        self._test_convert_document("example-html-input-009.html")

    def test_example_010(self):
        self._test_convert_document("example-html-input-010.html")

    def _test_convert_document(self, file_to_convert: str):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        txt: str = ""
        path_to_pdf = Path(__file__).parent / file_to_convert
        html_element: ET.Element = PDFToHTML.convert_pdf_to_html(path_to_pdf)

        # store
        output_file = self.output_dir / (file_to_convert + ".pdf")
        with open(output_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)


if __name__ == "__main__":
    unittest.main()
