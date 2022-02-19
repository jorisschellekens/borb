import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import X11Color
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Alignment, Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteTableWithNonBlackParagraphs(unittest.TestCase):
    """
    This test creates a PDF with a Table in it. This Table contains Paragraphs in different colors.
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

    def test_write_document(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # set layout
        layout = SingleColumnLayout(page)

        # write test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a Table in it. This Table contains Paragraphs in different colors."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        my_dict = {
            " ": ["A Error", "B Error", "C Error", "D Error"],
            "lab1": [0.34, 0.23, 0.80, 0.79],
            "lab2": [0.53, 0.38, 0.96, 1.25],
            "lab3": [0.40, 0.27, 0.68, 0.93],
        }

        colors = {
            0: X11Color("Green"),
            0.25: X11Color("Yellow"),
            0.5: X11Color("Orange"),
            0.75: X11Color("Red"),
        }

        table = Table(number_of_rows=4, number_of_columns=5)
        table.add(Paragraph(" ", respect_spaces_in_text=True))
        for h in my_dict[" "]:
            table.add(Paragraph(text=h, font="Helvetica-Bold", font_size=Decimal(12)))
        for name, row in [(k, v) for k, v in my_dict.items() if k != " "]:
            table.add(Paragraph(name))
            for v in row:
                c = X11Color("Green")
                for b, bc in colors.items():
                    if v > b:
                        c = bc
                table.add(
                    Paragraph(
                        str(v), font_color=c, horizontal_alignment=Alignment.CENTERED
                    )
                )

        # set border
        table.set_border_width_on_all_cells(Decimal(0.2))

        # set padding
        table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        # add to layout
        layout.add(Paragraph("This table contains all measurands for 3 lab-sessions:"))
        layout.add(table)

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
