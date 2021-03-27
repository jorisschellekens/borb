import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.layout_element import Alignment
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-alphabet-number-code-puzzle.log"),
    level=logging.DEBUG,
)


class TestWriteAlphabetNumberCodePuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-write-alphabet-number-code-puzzle"
        )

    def _build_table_for_sentence(self, sentence: str) -> Table:
        t = Table(number_of_columns=len(sentence), number_of_rows=3)
        for c in sentence:
            if c in [".", "?", "!", ",", " "]:
                t.add(
                    TableCell(
                        Paragraph(c, respect_spaces_in_text=True),
                        background_color=X11Color("SlateGray"),
                    )
                )
            else:
                num = ord(c.upper()) - ord("A") + 1
                t.add(
                    Paragraph(
                        str(num),
                        font_size=Decimal(6),
                        text_alignment=Alignment.CENTERED,
                    )
                )

        for c in sentence:
            t.add(Paragraph(" ", respect_spaces_in_text=True))

        for c in sentence:
            t.add(
                TableCell(
                    Paragraph(" ", respect_spaces_in_text=True),
                    border_top=False,
                    border_left=False,
                    border_right=False,
                )
            )

        t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        return t

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
                "Secret Code Puzzle",
                font_size=Decimal(20),
                font_color=X11Color("YellowGreen"),
            )
        )

        # add text
        layout.add(
            Paragraph(
                """
                There are three riddles below written in a secret code.
                Can you unravel them?
                Once you have, copy the sentence on the line underneath the code.
                
                Hint: Each letter of the alphabet has been replaced by a number. 
                All the riddles use the same code.
                """,
                respect_newlines_in_text=True,
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        # add grid
        for s in sentences:
            layout.add(self._build_table_for_sentence(s))
            layout.add(Paragraph(" ", respect_spaces_in_text=True))

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
