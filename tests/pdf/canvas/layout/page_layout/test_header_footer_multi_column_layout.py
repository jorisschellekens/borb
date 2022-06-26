import random
import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf import PageLayout
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.page_layout.header_footer_multi_column_layout import (
    HeaderFooterMultiColumnLayout,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.lipsum.lipsum import Lipsum
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestMarginAndPadding(unittest.TestCase):
    """
    This test creates a PDF with multiple pages.
    """

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

    def _add_header(self, page: Page, rectangle: Rectangle) -> None:
        Paragraph(
            """
            Joris Schellekens
            borb (ez)
            Belgium
            """,
            font_size=Decimal(10),
            font_color=HexColor("D3D3D3"),
            respect_newlines_in_text=True,
        ).layout(page, rectangle)

    def _add_footer(self, page: Page, rectangle: Rectangle) -> None:
        Paragraph(
            """
            page X / Y
            confidential
            """,
            font_size=Decimal(10),
            font_color=HexColor("D3D3D3"),
            respect_newlines_in_text=True,
        ).layout(page, rectangle)

    def test_set_header_and_footer(self):

        # create document
        pdf = Document()

        # add test information
        page = Page()
        pdf.add_page(page)

        # init layout
        l: PageLayout = HeaderFooterMultiColumnLayout(
            page,
            vertical_margin=Decimal(12),
            number_of_columns=1,
            header_callable=self._add_header,
            footer_callable=self._add_footer,
        )

        # add content
        random.seed(0)
        for _ in range(20):
            l.add(Paragraph(Lipsum.generate_lipsum_text(random.choice([4, 5, 6]))))

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_set_header(self):

        # create document
        pdf = Document()

        # add test information
        page = Page()
        pdf.add_page(page)

        # init layout
        l: PageLayout = HeaderFooterMultiColumnLayout(
            page,
            vertical_margin=Decimal(12),
            number_of_columns=1,
            header_callable=self._add_header,
        )

        # add content
        random.seed(0)
        for _ in range(20):
            l.add(Paragraph(Lipsum.generate_lipsum_text(random.choice([4, 5, 6]))))

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_set_footer(self):

        # create document
        pdf = Document()

        # add test information
        page = Page()
        pdf.add_page(page)

        # init layout
        l: PageLayout = HeaderFooterMultiColumnLayout(
            page,
            vertical_margin=Decimal(12),
            number_of_columns=1,
            footer_callable=self._add_footer,
        )

        # add content
        random.seed(0)
        for _ in range(20):
            l.add(Paragraph(Lipsum.generate_lipsum_text(random.choice([4, 5, 6]))))

        # determine output location
        out_file = self.output_dir / "output_003.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)