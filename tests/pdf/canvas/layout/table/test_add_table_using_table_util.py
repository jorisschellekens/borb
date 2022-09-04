import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.table.table_util import TableUtil
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestAddTableUsingTableUtil(unittest.TestCase):
    """
    This test creates a PDF with a Table in it.
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

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        layout = SingleColumnLayout(page)

        # write test information
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
                    "This test creates a PDF with a Table in it. This table was creating using TableUtil."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write Table
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Country", "GDP"],
                    ["United States", 93863.851],
                    ["China", 19911.593],
                    ["Japan", 4912.147],
                    ["India", 3534.743],
                ],
                header_row=True,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_001.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_write_document_002(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        layout = SingleColumnLayout(page)

        # write test information
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
                    "This test creates a PDF with a Table in it. This table was creating using TableUtil."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write Table
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Country", "GDP"],
                    ["United States", 93863.851],
                    ["China", 19911.593],
                    ["Japan", 4912.147],
                    ["India", 3534.743],
                ],
                header_row=True,
                round_to_n_digits=1,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_002.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_write_document_003(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        layout = SingleColumnLayout(page)

        # write test information
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
                    "This test creates a PDF with a Table in it. This table was creating using TableUtil."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write Table
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Country", "GDP"],
                    ["United States", 93863.851],
                    ["China", 19911.593],
                    ["Japan", 4912.147],
                    ["India", 3534.743],
                ],
                header_row=False,
                header_col=True,
                round_to_n_digits=1,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_003.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_write_document_004(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        layout = SingleColumnLayout(page)

        # write test information
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
                    "This test creates a PDF with a Table in it. This table was creating using TableUtil."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write Table
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Country", "GDP"],
                    ["United States", 93863.851],
                    ["China", 19911.593],
                    ["Japan", 4912.147],
                    ["India", 3534.743],
                ],
                header_row=False,
                header_col=False,
                round_to_n_digits=1,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_004.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
