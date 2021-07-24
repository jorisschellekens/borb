import unittest
from pathlib import Path

from borb.pdf.document import Document
from borb.pdf.pdf import PDF
from borb.toolkit.export.markdown_to_pdf.markdown_to_pdf import MarkdownToPDF


class TestExportMarkdownToPDF(unittest.TestCase):
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

    def test_document_001(self):
        self._test_document("example-markdown-input-001.md")

    def test_document_002(self):
        self._test_document("example-markdown-input-002.md")

    def test_document_003(self):
        self._test_document("example-markdown-input-003.md")

    def test_document_004(self):
        self._test_document("example-markdown-input-004.md")

    def test_document_005(self):
        self._test_document("example-markdown-input-005.md")

    def test_document_006(self):
        self._test_document("example-markdown-input-006.md")

    def test_document_007(self):
        self._test_document("example-markdown-input-007.md")

    def test_document_008(self):
        self._test_document("example-markdown-input-008.md")

    def test_document_009(self):
        self._test_document("example-markdown-input-009.md")

    def _test_document(self, file_to_convert: str):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        txt: str = ""
        path_to_json = Path(__file__).parent / file_to_convert
        with open(path_to_json, "r") as json_file_handle:
            txt = json_file_handle.read()

        # convert
        document: Document = MarkdownToPDF.convert_markdown_to_pdf(txt)

        # store
        output_file = self.output_dir / (file_to_convert + ".pdf")
        with open(output_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)


if __name__ == "__main__":
    unittest.main()
