import unittest
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import SingleColumnLayoutWithOverflow
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.document.document import Document
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from borb.toolkit.export.markdown_to_pdf.markdown_to_pdf import MarkdownToPDF
from tests.test_case import TestCase


class TestExportMarkdownToPDF(TestCase):
    def test_document_001(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-001.md"
        )

    def test_document_011(self):

        input_file: Path = (
            self.get_artifacts_directory() / "example-markdown-input-011.md"
        )
        with open(input_file, "r") as json_file_handle:
            txt = json_file_handle.read()

        # convert
        document: Document = Document()
        page: Page = Page(
            width=PageSize.A4_PORTRAIT.value[0], height=PageSize.A4_PORTRAIT.value[1]
        )
        document.add_page(page)
        layout: PageLayout = SingleColumnLayoutWithOverflow(page)
        layout._margin_top = Decimal(12)
        layout._margin_right = Decimal(0)
        layout.margin_bottom = Decimal(12)
        layout._margin_left = Decimal(0)

        # path to _font
        font_path: Path = self.get_artifacts_directory() / "SimHei.ttf"
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
        out_file = input_file.parent / (input_file.stem + ".pdf")
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)
        self.compare_visually_to_ground_truth(out_file)
        self.check_pdf_using_validator(out_file)

    def test_document_002(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-002.md"
        )

    def test_document_003(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-003.md"
        )

    def test_document_004(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-004.md"
        )

    def test_document_005(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-005.md"
        )

    def test_document_006(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-006.md"
        )

    def test_document_007(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-007.md"
        )

    def test_document_008(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-008.md"
        )

    def test_document_009(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-009.md"
        )

    def test_document_010(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-010.md"
        )

    def test_document_012(self):
        self._export_markdown_to_pdf(
            self.get_artifacts_directory() / "example-markdown-input-012.md"
        )

    def _export_markdown_to_pdf(self, input_file: Path):

        txt: str = ""
        with open(input_file, "r") as json_file_handle:
            txt = json_file_handle.read()

        # convert
        document: Document = Document()
        page: Page = Page(
            width=PageSize.A4_PORTRAIT.value[0], height=PageSize.A4_PORTRAIT.value[1]
        )
        document.add_page(page)
        layout: PageLayout = SingleColumnLayoutWithOverflow(page)
        layout._margin_top = Decimal(12)
        layout._margin_right = Decimal(0)
        layout.margin_bottom = Decimal(12)
        layout._margin_left = Decimal(0)
        layout.add(MarkdownToPDF.convert_markdown_to_layout_element(txt))

        # store
        out_file = input_file.parent / (input_file.stem + ".pdf")
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)
        self.compare_visually_to_ground_truth(out_file)
        self.check_pdf_using_validator(out_file)


if __name__ == "__main__":
    unittest.main()
