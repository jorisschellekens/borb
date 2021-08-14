import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteFlexiTable(unittest.TestCase):
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

    def test_write_document(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # write test information
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
                    "This test creates a PDF with a Table in it. The columns in the Table have a preferred width and height."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t = FlexibleColumnWidthTable(
            number_of_rows=16,
            number_of_columns=27,
            horizontal_alignment=Alignment.CENTERED,
            padding_top=Decimal(5),
        )

        def _insert_n_blanks(n: int):
            for _ in range(0, n):
                t.add(
                    TableCell(
                        Paragraph(" "),
                        border_width=Decimal(0),
                        preferred_width=Decimal(16),
                        preferred_height=Decimal(16),
                    )
                )

        def _insert_n_blanks_all_borders(n: int):
            for _ in range(0, n):
                t.add(
                    TableCell(
                        Paragraph(" "),
                        preferred_width=Decimal(16),
                        preferred_height=Decimal(16),
                    )
                )

        def _insert_number(n: int):
            t.add(
                TableCell(
                    Paragraph(str(n), text_alignment=Alignment.CENTERED),
                    preferred_width=Decimal(16),
                    preferred_height=Decimal(16),
                )
            )

        # row 0
        _insert_n_blanks(17)
        _insert_number(1)
        _insert_n_blanks(9)

        # row 1
        _insert_n_blanks(10)
        _insert_number(1)
        _insert_n_blanks(3)
        _insert_number(1)
        _insert_n_blanks(2)
        _insert_number(1)
        _insert_number(3)
        _insert_n_blanks(1)
        _insert_number(1)
        _insert_n_blanks(1)
        _insert_number(1)
        _insert_n_blanks(2)
        _insert_number(1)
        _insert_n_blanks(1)

        # row 2
        _insert_n_blanks(8)
        for k in [0, 8, 1, 4, 0, 7, 1, 0, 5, 1, 1, 0, 1, 3, 1, 0, 7, 1, 0]:
            _insert_number(k)

        # empty row
        _insert_n_blanks(27)

        # row 3
        _insert_n_blanks(6)
        _insert_number(0)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 4
        _insert_n_blanks(5)
        _insert_number(1)
        _insert_number(1)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 5
        _insert_n_blanks(5)
        _insert_number(1)
        _insert_number(1)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 6
        _insert_n_blanks(1)
        for k in [3, 2, 3, 1, 1, 2]:
            _insert_number(k)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 7
        for k in [1, 1, 1, 1, 1, 1, 1]:
            _insert_number(k)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 8
        _insert_n_blanks(1)
        for k in [1, 1, 1, 3, 1, 1]:
            _insert_number(k)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 9
        _insert_n_blanks(2)
        for k in [3, 1, 1, 1, 1]:
            _insert_number(k)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 10
        _insert_n_blanks(1)
        for k in [1, 2, 3, 1, 1, 2]:
            _insert_number(k)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        # row 11, 12, 13
        for _ in range(0, 3):
            _insert_n_blanks(6)
            _insert_number(1)
            _insert_n_blanks(1)
            _insert_n_blanks_all_borders(19)

        # row 14
        _insert_n_blanks(6)
        _insert_number(0)
        _insert_n_blanks(1)
        _insert_n_blanks_all_borders(19)

        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf")
