import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteBattleship(unittest.TestCase):
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

    def test_write_battleship_puzzle(self):

        doc: Document = Document()
        page: Page = Page()
        doc.append_page(page)

        font: Font = TrueTypeFont.true_type_font_from_file(
            Path(__file__).parent / "Pacifico.ttf"
        )

        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            Heading(
                "Battleship",
                font=font,
                font_size=Decimal(20),
                font_color=HexColor("f1cd2e"),
            )
        )

        layout.add(
            Paragraph(
                """
            In Battleship, an armada of battleships is hidden in a square grid of 10×10 small squares. 
            The armada includes one battleship four squares long, two cruisers three squares long, 
            three destroyers two squares long, and four submarines one square in size.
            Each ship occupies a number of contiguous squares on the grid, arranged horizontally or vertically. 
            """,
                hyphenation=Hyphenation("en-gb"),
            )
        )

        layout.add(
            Paragraph(
                """
            The ships are placed so that no ship touches any other ship, not even diagonally.
            The goal of the puzzle is to discover where the ships are located. 
            A grid may start with clues in the form of squares that have already been solved, showing a submarine, 
            an end piece of a ship, a middle piece of a ship, or water. 
            Each row and column also has a number beside it, indicating the number of squares occupied by ship parts in that row or column, 
            respectively.
            """,
                hyphenation=Hyphenation("en-gb"),
            )
        )

        t: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_rows=11,
            number_of_columns=11,
            horizontal_alignment=Alignment.CENTERED,
        )
        x_clues = [1, 2, 1, 3, 2, 2, 3, 1, 5, 0]
        y_clues = [3, 2, 2, 4, 2, 1, 1, 2, 3, 0]

        for i in range(0, 10):
            for _ in range(0, 10):
                t.add(
                    TableCell(
                        Paragraph(" "),
                        preferred_width=Decimal(20),
                        preferred_height=Decimal(20),
                    )
                )
            t.add(
                TableCell(
                    Paragraph(str(y_clues[i]), text_alignment=Alignment.CENTERED),
                    preferred_width=Decimal(20),
                    preferred_height=Decimal(20),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    padding_top=Decimal(4),
                )
            )

        for i in range(0, 10):
            t.add(
                TableCell(
                    Paragraph(str(x_clues[i]), text_alignment=Alignment.CENTERED),
                    preferred_width=Decimal(20),
                    preferred_height=Decimal(20),
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                    padding_top=Decimal(4),
                )
            )

        t.add(
            TableCell(
                Paragraph(" "),
                preferred_width=Decimal(20),
                preferred_height=Decimal(20),
                border_top=False,
                border_right=False,
                border_bottom=False,
                border_left=False,
            )
        )

        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output.pdf")
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf")
