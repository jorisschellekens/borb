import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf import (
    FixedColumnWidthTable,
    FlexibleColumnWidthTable,
    TableCell,
)
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth

unittest.TestLoader.sortTestMethodsUsing = None


class TestWriteTableWithRoundedBorders(unittest.TestCase):
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

    def test_write_table_with_borders_000(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.append_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # test information
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Table in it. The Table has no rounded borders."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add a Table object
        t = (
            FlexibleColumnWidthTable(
                number_of_rows=2,
                number_of_columns=2,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor Sit"))
            .add(Paragraph("Amet"))
            .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        )
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output_000.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_table_with_borders_001(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.append_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # test information
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Table in it. The Table has 1 rounded border."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add a Table object
        t = (
            FlexibleColumnWidthTable(
                number_of_rows=2,
                number_of_columns=2,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
            .add(TableCell(Paragraph("Lorem"), border_radius_top_left=Decimal(20)))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor Sit"))
            .add(Paragraph("Amet"))
            .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        )
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_table_with_borders_002(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.append_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # test information
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Table in it. The Table has 2 rounded borders."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add a Table object
        t = (
            FlexibleColumnWidthTable(
                number_of_rows=2,
                number_of_columns=2,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
            .add(TableCell(Paragraph("Lorem"), border_radius_top_left=Decimal(20)))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor Sit"))
            .add(TableCell(Paragraph("Amet"), border_radius_bottom_right=Decimal(20)))
            .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        )
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_table_with_borders_003(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.append_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # test information
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Table in it. The Table has rounded borders."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add a Table object
        t = (
            FlexibleColumnWidthTable(
                number_of_rows=2,
                number_of_columns=2,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor Sit"))
            .add(Paragraph("Amet"))
            .outer_borders_rounded(Decimal(10))
            .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        )
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output_003.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_table_with_borders_004(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.append_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # test information
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an Table in it. The Table has rounded borders."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add a Table object
        t = (
            FlexibleColumnWidthTable(
                number_of_rows=2,
                number_of_columns=2,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor Sit"))
            .add(Paragraph("Amet"))
            .outer_borders()
            .outer_borders_rounded(Decimal(10))
            .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        )
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output_004.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)
