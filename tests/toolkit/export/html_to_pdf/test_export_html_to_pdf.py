import unittest
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import Page, SingleColumnLayoutWithOverflow
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from borb.toolkit.export.html_to_pdf.html_to_pdf import HTMLToPDF
from tests.test_case import TestCase


class TestExportHTMLToPDF(TestCase):
    def test_example_000(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_000.html"
        )

    def test_example_001(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_001.html"
        )

    def test_example_002(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_002.html"
        )

    def test_example_003(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_003.html"
        )

    def test_example_004(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_004.html"
        )

    def test_example_005(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_005.html"
        )

    def test_example_006(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_006.html"
        )

    def test_example_007(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_007.html"
        )

    def test_example_008(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_008.html",
            width=PageSize.A3_LANDSCAPE.value[0],
            height=PageSize.A3_LANDSCAPE.value[1],
        )

    def test_example_009(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_009.html"
        )

    @unittest.skip
    def test_example_010(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_010.html"
        )

    def test_example_011(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_011.html"
        )

    def test_example_012(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_012.html"
        )

    def test_example_013(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_013.html"
        )

    def test_example_014(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_014.html"
        )

    def test_example_015(self):
        self._export_html_to_pdf(
            self.get_artifacts_directory() / "example_html_input_015.html"
        )

    def _export_html_to_pdf(
        self,
        input_file: Path,
        width: Decimal = PageSize.A4_PORTRAIT.value[0],
        height: Decimal = PageSize.A4_PORTRAIT.value[1],
    ):

        txt: str = ""
        with open(input_file, "r") as fh:
            txt = fh.read()

        # convert
        document: Document = Document()
        page: Page = Page(width=width, height=height)
        document.add_page(page)
        layout: PageLayout = SingleColumnLayoutWithOverflow(page)
        layout._margin_top = Decimal(12)
        layout._margin_right = Decimal(0)
        layout.margin_bottom = Decimal(12)
        layout._margin_left = Decimal(0)
        layout.add(HTMLToPDF.convert_html_to_layout_element(txt))

        # store
        out_file = input_file.parent / (input_file.stem + ".pdf")
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)
        self.compare_visually_to_ground_truth(out_file)
        self.check_pdf_using_validator(out_file)


if __name__ == "__main__":
    unittest.main()
