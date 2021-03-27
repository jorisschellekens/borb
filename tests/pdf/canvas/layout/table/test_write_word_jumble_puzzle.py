import logging
import random
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-word-scramble-puzzle.log"),
    level=logging.DEBUG,
)


class TestWriteWordScramblePuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-word-scramble-puzzle")

    def test_write_document(self):

        words = [
            "COW",
            "PUPPY",
            "TURTLE",
            "PARROT",
            "SNAKE",
            "GOLDFISH",
            "HAMSTER",
            "KITTEN",
            "TURKEY",
            "DOVE",
            "HORSE",
            "BEE" "RABBIT",
            "DUCK",
            "SHRIMP",
            "PIG",
            "GOAT",
            "CRAB",
            "DOG",
            "DEER",
            "CAT",
            "MOUSE",
            "ELEPHANT",
            "LION",
            "PENGUIN",
            "SPARROW",
            "STORK",
            "HAWK",
        ]

        pdf = Document()
        page = Page()
        pdf.append_page(page)

        # layout
        layout = MultiColumnLayout(page, number_of_columns=2)

        # add title
        layout.add(
            Paragraph(
                """
                Word scrambles or anagrams are an excellent way of helping children 
                with their spelling as they have to recognise letter patterns. 
                They are also a fun way of testing knowledge on a subject. 
                We have word scrambles on lots of topics ready to print for home or classroom.
                """,
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        # add table
        t = Table(number_of_rows=len(words), number_of_columns=2)
        for i, w in enumerate(words):
            # shuffle word
            permuted_word = w
            while permuted_word == w:
                letters = [x for x in w]
                random.shuffle(letters)
                permuted_word = "".join([x for x in letters])
            t.add(
                TableCell(
                    Paragraph(str(i + 1) + ". " + permuted_word),
                    border_top=False,
                    border_right=False,
                    border_left=False,
                    border_bottom=False,
                )
            )
            # empty column
            t.add(
                TableCell(
                    Paragraph(""),
                    border_top=False,
                    border_right=False,
                    border_left=False,
                )
            )

        layout.add(t)

        # go to next column
        layout.switch_to_next_column()

        # add title
        layout.add(
            Paragraph(
                "Word Scramble",
                font_size=Decimal(20),
                font_color=X11Color("YellowGreen"),
            )
        )

        # add Image
        layout.add(
            Image(
                "https://www.how-to-draw-funny-cartoons.com/images/cartoon-tree-012.jpg"
            )
        )

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
