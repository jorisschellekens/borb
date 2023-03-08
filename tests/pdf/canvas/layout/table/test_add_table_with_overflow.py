import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import PageLayout, FlexibleColumnWidthTable
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.single_column_layout_with_overflow import (
    SingleColumnLayoutWithOverflow,
)
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
    FixedColumnWidthTable,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestAddTableWithOverflow(unittest.TestCase):
    """
    This test creates a PDF with a Table in it. This Table contains too many rows to fit on a single Page.
    By using SingleColumnLayoutWithOverflow, the Table is automatically split.
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

    def test_add_table_with_overflow(self):

        # create Document
        doc: Document = Document()

        # create Page
        page: Page = Page()
        doc.add_page(page)

        # create PageLayout
        layout: PageLayout = SingleColumnLayoutWithOverflow(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a simple Table in it. The table is too large to fit on a single Page."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # build Table
        n: int = 30
        t: Table = FixedColumnWidthTable(number_of_rows=n, number_of_columns=2)
        for i in range(1, n + 1):
            t.add(Paragraph("row %d, col 0" % i))
            t.add(Paragraph("row %d, col 1" % i))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        # add
        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output_001.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_table_with_overflow_001(self):

        # create empty PDF
        pdf = Document()

        # add Page
        page = Page(PageSize.A4_LANDSCAPE.value[0], PageSize.A4_LANDSCAPE.value[1])
        pdf.add_page(page)

        # set PageLayout
        layout = SingleColumnLayoutWithOverflow(
            page, horizontal_margin=Decimal(5), vertical_margin=Decimal(5)
        )

        # add FlexibleColumnWidthTable
        table = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=72)
        layout.add(table)

        # determine output location
        out_file = self.output_dir / ("output_002.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
