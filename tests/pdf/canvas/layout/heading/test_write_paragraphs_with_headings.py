import random
import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import (
    SingleColumnLayout,
    MultiColumnLayout,
)
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestWriteParagraphsWithHeadings(unittest.TestCase):
    """
    This test creates a PDF with several Heading objects in it.
    Headings are essentially Paragraphs that also influence the contents-pane (in Adobe).
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

        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with several Heading objects in it. Headings are essentially Paragraphs that also influence the contents-pane (in Adobe)."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        page = Page()
        pdf.append_page(page)
        layout = MultiColumnLayout(page, number_of_columns=2)

        layout.add(
            Heading(
                "Lorem Ipsum",
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                font_color=HexColor("0b3954"),
            )
        )
        layout.add(
            Paragraph(
                "Cicero",
                font="Helvetica-Oblique",
                font_size=Decimal(8),
                font_color=HexColor("56cbf9"),
            )
        )
        N: int = 16
        for i in range(0, N):
            print("writing %d / %d" % (i + 1, N))
            layout.add(
                Heading(
                    "Lorem Ipsum",
                    font_size=Decimal(18.2),
                    font="Helvetica-Bold",
                    font_color=HexColor("f1cd2e"),
                    outline_level=1,
                )
            )
            for _ in range(0, random.choice([10, 20, 3])):
                layout.add(
                    Paragraph(
                        """
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum
                        """,
                        font_size=Decimal(12),
                        horizontal_alignment=Alignment.LEFT,
                    )
                )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
