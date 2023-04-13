import datetime
import unittest
from _decimal import Decimal
from pathlib import Path

from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    PageLayout,
    FixedColumnWidthTable,
    Table,
    Image,
    Paragraph,
    Alignment,
    PDF,
    FlexibleColumnWidthTable,
    HexColor,
)
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestTableWithLayoutElementWithVerticalAlignment(unittest.TestCase):
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

    def test_create_table_with_layout_element_with_vertical_alignment_000(self):
        doc: Document = Document()

        page: Page = Page()
        doc.add_page(page)

        page_layout: PageLayout = SingleColumnLayout(page)

        # write test info
        page_layout.add(
            FixedColumnWidthTable(
                number_of_columns=2,
                number_of_rows=3,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a Table in it, LayoutElements in the Table have their vertical alignment set."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        table: Table = FixedColumnWidthTable(number_of_columns=4, number_of_rows=1)
        table.add(
            Image(
                "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
                width=Decimal(100),
                height=Decimal(100),
            )
        )
        table.add(Paragraph("TOP"))
        table.add(Paragraph("MIDDLE", vertical_alignment=Alignment.MIDDLE))
        table.add(Paragraph("BOTTOM", vertical_alignment=Alignment.BOTTOM))
        page_layout.add(table)

        # determine output location
        out_file = self.output_dir / ("output_000.pdf")
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_create_table_with_layout_element_with_vertical_alignment_001(self):
        doc: Document = Document()

        page: Page = Page()
        doc.add_page(page)

        page_layout: PageLayout = SingleColumnLayout(page)

        # write test info
        page_layout.add(
            FixedColumnWidthTable(
                number_of_columns=2,
                number_of_rows=3,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a Table in it, LayoutElements in the Table have their vertical alignment set."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        table: Table = FlexibleColumnWidthTable(number_of_columns=4, number_of_rows=1)
        table.add(
            Image(
                "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
                width=Decimal(100),
                height=Decimal(100),
            )
        )
        table.add(Paragraph("TOP"))
        table.add(Paragraph("MIDDLE", vertical_alignment=Alignment.MIDDLE))
        table.add(Paragraph("BOTTOM", vertical_alignment=Alignment.BOTTOM))
        page_layout.add(table)

        # determine output location
        out_file = self.output_dir / ("output_001.pdf")
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
