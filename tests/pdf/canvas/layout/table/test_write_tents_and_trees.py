import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteTentsAndTrees(unittest.TestCase):
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

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

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
                    "This test creates a PDF with a Table in it. This Table has some emoji in it."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write puzzle title
        font: Font = TrueTypeFont.true_type_font_from_file(
            Path(__file__).parent / "Pacifico.ttf"
        )
        layout.add(
            Paragraph(
                "Tents and Trees",
                font_color=HexColor("#f1cd2e"),
                font=font,
                font_size=Decimal(23),
            )
        )

        # write puzzle information
        layout.add(
            Paragraph(
                """
                You get a grid that represents a campsite. 
                There are a number of trees on the campsite. 
                You as a campsite manager must find a spot for the tent of each visitor that meets the following requirements:
                """
            )
        )
        layout.add(
            UnorderedList()
            .add(
                Paragraph(
                    "A tree must be immediately next to each tent (diagonal is not allowed)."
                )
            )
            .add(
                Paragraph(
                    "In total there are as many tents as trees. So every tent has its own tree."
                )
            )
            .add(
                Paragraph(
                    "The numbers outside the grid indicate how many tents there are in the relevant row or column."
                )
            )
            .add(
                Paragraph(
                    "Tents never touch each other: neither horizontally nor vertically nor diagonally."
                )
            )
            .add(
                Paragraph(
                    "A tent can make contact with multiple trees, but is only connected to one."
                )
            )
        )

        # write grid
        w = Decimal(20)
        grid = FlexibleColumnWidthTable(
            number_of_rows=11,
            number_of_columns=11,
            margin_top=Decimal(5),
            horizontal_alignment=Alignment.CENTERED,
        )
        h_clues = [3, 2, 2, 1, 2, 2, 1, 2, 2, 3]
        v_clues = [3, 1, 1, 3, 1, 3, 2, 2, 0, 4]
        tree_layout = """
        __________
        x_____x__x
        ____x_____
        _x____x___
        ____x____x
        xx___x__x_
        ___x___x__
        _x_______x
        __x_____x_
        _x____x___
        """
        tree_layout = tree_layout.replace("\n", "").replace(" ", "")
        grid.add(TableCell(Paragraph(" "), preferred_height=w, preferred_width=w))
        for i in h_clues:
            grid.add(
                TableCell(Paragraph(str(i)), preferred_height=w, preferred_width=w)
            )
        for i in range(0, 10):
            grid.add(
                TableCell(
                    Paragraph(str(v_clues[i])), preferred_height=w, preferred_width=w
                )
            )
            for j in range(0, 10):
                if tree_layout[i * 10 + j] == "_":
                    grid.add(
                        TableCell(Paragraph(" "), preferred_height=w, preferred_width=w)
                    )
                else:
                    grid.add(
                        TableCell(
                            Emojis.EVERGREEN_TREE.value,
                            preferred_height=w,
                            preferred_width=w,
                        )
                    )

        grid.set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
        layout.add(grid)

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
