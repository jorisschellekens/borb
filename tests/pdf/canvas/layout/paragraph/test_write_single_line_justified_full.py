import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.square_annotation import SquareAnnotation
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import (
    SingleColumnLayout,
    MultiColumnLayout,
)
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteSingleLineJustifiedFull(unittest.TestCase):
    """
    This test creates a PDF with a Paragraph object in it. The Paragraph is aligned BOTTOM, CENTERED.
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

    def test_write_document_001(self):
        doc: Document = Document()
        page: Page = Page()
        doc.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a Paragraph object in it. The Paragraph is aligned TOP, CENTERED."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        p: Paragraph = Paragraph(
            "Hello World!", horizontal_alignment=Alignment.JUSTIFIED
        )

        # the next line of code uses absolute positioning
        # fmt: off
        r: Rectangle = Rectangle(
            Decimal(59),                    # x: 0 + page_margin
            Decimal(848 - 84 - 200 - 100),  # y: page_height - page_margin - y - height_of_textbox
            Decimal(595 - 59 * 2),          # width: page_width - 2 * page_margin
            Decimal(100),                   # height
        )
        # fmt: on

        # this is a quick and dirty way to draw a rectangle on the page
        page.append_annotation(SquareAnnotation(r, stroke_color=HexColor("f1cd2e")))

        # add the paragraph to the page
        p.layout(page, r)

        # determine output location
        out_file = self.output_dir / "output_001.pdf"
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_001.pdf")

    def test_write_document_002(self):

        doc: Document = Document()
        page: Page = Page()
        doc.append_page(page)

        # add test information
        page_layout_001 = SingleColumnLayout(page)
        page_layout_001.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a Paragraph object in it. The text in the Paragraph needs to be split and justified."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # switch to MultiColumnLayout
        page_layout_002: PageLayout = MultiColumnLayout(page, 2)

        # mark the top section as off limits
        max_y: Decimal = Decimal(PageSize.A4_PORTRAIT.value[1] - 170)
        page_layout_002._page_height = max_y
        page_layout_002._previous_element_y = max_y - page_layout_002._vertical_margin

        p: Paragraph = Paragraph(
            """
            The License to Use the Software is subject to You having fully
            paid up the license fee as specified in a separate quotation
            (“Order” or “Invoice”) attached hereto. You may only install,
            access, use the Software or works derived therefrom up to the
            number of licenses granted in the Order or Invoice.
            """,
            font_size=Decimal(8),
            horizontal_alignment=Alignment.JUSTIFIED,
        )
        page_layout_002.add(p)

        # determine output location
        out_file = self.output_dir / "output_002.pdf"
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")
