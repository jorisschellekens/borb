import unittest
from pathlib import Path

from borb.pdf.document.document import Document
from borb.pdf.pdf import PDF
from borb.toolkit.export.html_to_pdf.html_to_pdf import HTMLToPDF
from tests.test_util import compare_visually_to_ground_truth


class TestExportHTMLToPDF(unittest.TestCase):
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
        self._test_convert_document("example_html_input_000.html")

    def test_example_001(self):
        self._test_convert_document("example_html_input_001.html")

    def test_example_002(self):
        self._test_convert_document("example_html_input_002.html")

    def test_example_003(self):
        self._test_convert_document("example_html_input_003.html")

    def test_example_004(self):
        self._test_convert_document("example_html_input_004.html")

    def test_example_005(self):
        self._test_convert_document("example_html_input_005.html")

    def test_example_006(self):
        self._test_convert_document("example_html_input_006.html")

    def test_example_007(self):
        self._test_convert_document("example_html_input_007.html")

    def test_example_008(self):
        self._test_convert_document("example_html_input_008.html")

    def test_example_009(self):
        self._test_convert_document("example_html_input_009.html")

    def test_example_010(self):
        self._test_convert_document("example_html_input_010.html")

    def test_example_011(self):
        self._test_convert_document("example_html_input_011.html")

    def test_example_012(self):
        self._test_convert_document("example_html_input_012.html")

    def test_example_013(self):
        self._test_convert_document("example_html_input_013.html")

    def test_example_014(self):
        self._test_convert_document("example_html_input_014.html")

    def _test_convert_document(self, file_to_convert: str):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        txt: str = ""
        path_to_json = Path(__file__).parent / file_to_convert
        with open(path_to_json, "r") as json_file_handle:
            txt = json_file_handle.read()

        # convert
        document: Document = HTMLToPDF.convert_html_to_pdf(txt)

        # store
        output_file = self.output_dir / (file_to_convert.replace(".html", ".pdf"))
        with open(output_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)

        # compare visually
        compare_visually_to_ground_truth(output_file)


if __name__ == "__main__":
    unittest.main()
