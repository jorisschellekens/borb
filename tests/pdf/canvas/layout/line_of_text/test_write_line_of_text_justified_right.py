import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.square_annotation import SquareAnnotation
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestWriteLineOfTextJustifiedRight(unittest.TestCase):
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
                    "This test creates a PDF with several LineOfText objects in it, horizontal alignment set to RIGHT."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        rs = []
        for i, s in enumerate(
            [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut",
                "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco",
                "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in",
                "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat",
                "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            ]
        ):
            r = LineOfText(
                s,
                font_size=Decimal(10),
                horizontal_alignment=Alignment.RIGHT,
            ).layout(
                page,
                Rectangle(
                    Decimal(59), Decimal(550 - 24 * i), Decimal(476), Decimal(24)
                ),
            )
            rs.append(r)

        # add rectangle annotation
        page.append_annotation(
            SquareAnnotation(
                Rectangle(
                    Decimal(59), Decimal(550 - 24 * 4), Decimal(476), Decimal(24 * 5)
                ),
                stroke_color=HexColor("f1cd2e"),
            )
        )

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

    def test_write_single_line_of_text_with_annotation(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

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
                    "This test creates a PDF with a single LineOfText object in it, horizontal alignment set to RIGHT."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # Rectangle
        rect: Rectangle = Rectangle(
            Decimal(59), Decimal(550 - 24), Decimal(476), Decimal(24)
        )

        # Shape
        page.append_annotation(SquareAnnotation(rect, stroke_color=HexColor("000000")))

        # LineOfText
        LineOfText(
            "Lorem Ipsum Dolor Sit Amet",
            font_size=Decimal(10),
            background_color=X11Color("Gray"),
            border_color=X11Color("Black"),
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            horizontal_alignment=Alignment.RIGHT,
        ).layout(
            page,
            rect,
        )

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
