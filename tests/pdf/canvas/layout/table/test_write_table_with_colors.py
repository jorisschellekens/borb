import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-simple-table.log"), level=logging.DEBUG
)


class TestWriteTableWithColors(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-table-with-colors")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # set layout
        layout = SingleColumnLayout(page)

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
