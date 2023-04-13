import unittest
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import (
    Page,
    PageLayout,
    SingleColumnLayout,
    SingleColumnLayoutWithOverflow,
)
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.document.document import Document
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from borb.toolkit.export.markdown_to_pdf.markdown_to_pdf import MarkdownToPDF
from tests.test_util import check_pdf_using_validator, compare_visually_to_ground_truth


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

    def test_document_011(self):

        txt: str = ""
        file_to_convert: str = "example-markdown-input-011.md"
        path_to_json = Path(__file__).parent / file_to_convert
        with open(path_to_json, "r") as json_file_handle:
            txt = json_file_handle.read()

        # convert
        document: Document = Document()
        page: Page = Page(
            width=PageSize.A4_PORTRAIT.value[0], height=PageSize.A4_PORTRAIT.value[1]
        )
        document.add_page(page)
        layout: PageLayout = SingleColumnLayout(
            page, vertical_margin=Decimal(0), horizontal_margin=Decimal(12)
        )

        # path to _font
        font_path: Path = Path(__file__).parent / "SimHei.ttf"
        assert font_path.exists()

        # load font
        ttf = TrueTypeFont.true_type_font_from_file(font_path)

        # convert
        layout.add(
            MarkdownToPDF.convert_markdown_to_layout_element(
                txt, fallback_fonts_regular=[StandardType1Font("Helvetica"), ttf]
            )
        )

        # store
        out_file = self.output_dir / (file_to_convert + ".pdf")
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)
        check_pdf_using_validator(out_file)

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

    def test_document_010(self):
        self._test_document("example-markdown-input-010.md")

    def test_document_012(self):
        self._test_document("example-markdown-input-012.md")

    def _test_document(self, file_to_convert: str):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        txt: str = ""
        path_to_json = Path(__file__).parent / file_to_convert
        with open(path_to_json, "r") as json_file_handle:
            txt = json_file_handle.read()

        # convert
        document: Document = Document()
        page: Page = Page(
            width=PageSize.A4_PORTRAIT.value[0], height=PageSize.A4_PORTRAIT.value[1]
        )
        document.add_page(page)
        layout: PageLayout = SingleColumnLayoutWithOverflow(
            page, vertical_margin=Decimal(0), horizontal_margin=Decimal(12)
        )
        layout.add(MarkdownToPDF.convert_markdown_to_layout_element(txt))

        # store
        out_file = self.output_dir / (file_to_convert.replace(".md", ".pdf"))
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)

        check_pdf_using_validator(out_file)
        compare_visually_to_ground_truth(out_file)


if __name__ == "__main__":
    unittest.main()
