import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-reverse-the-words-code-puzzle.log"),
    level=logging.DEBUG,
)


class TestWriteWordScramblePuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-write-reverse-the-words-code-puzzle"
        )

    def test_write_document(self):

        sentences = [
            "THE BOAT WILL ARRIVE ON MONDAY",
            "SHE LIVES AT THE HOUSE WITH THE BLUE DOOR",
            "A FRIEND IN NEED IS A FRIEND INDEED",
            "AN APPLE A DAY KEEPS THE DOCTOR AWAY",
        ]

        pdf = Document()
        page = Page()
        pdf.append_page(page)

        # layout
        layout = SingleColumnLayout(page)

        # add title
        layout.add(
            Paragraph(
                "Reverse the words",
                font_size=Decimal(20),
                font_color=X11Color("YellowGreen"),
            )
        )

        # add text
        layout.add(
            Paragraph(
                """
                This is perhaps the simplest code to use and solve. 
                Simply read each word backwards.
                """,
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        # add grid
        t = Table(
            number_of_rows=len(sentences) * 2,
            number_of_columns=2,
            column_widths=[Decimal(1), Decimal(9)],
        )
        for i, s in enumerate(sentences):
            # code word
            coded_sentence = "".join(
                ["".join([y for y in reversed(x)]) + "   " for x in s.split(" ")]
            )
            t.add(
                TableCell(
                    Paragraph(str(i + 1) + "."),
                    border_top=False,
                    border_right=False,
                    border_left=False,
                    border_bottom=False,
                    row_span=2,
                )
            )
            t.add(
                TableCell(
                    Paragraph(coded_sentence, respect_spaces_in_text=True),
                    border_top=False,
                    border_right=False,
                    border_left=False,
                    border_bottom=False,
                )
            )
            t.add(
                TableCell(
                    Paragraph(".."),
                    border_top=False,
                    border_right=False,
                    border_left=False,
                    border_bottom=True,
                )
            )

        t.set_padding_on_all_cells(Decimal(15), Decimal(5), Decimal(5), Decimal(5))
        layout.add(t)

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
