import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import typing

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth

unittest.TestLoader.sortTestMethodsUsing = None


class TestInlineObjectIO(unittest.TestCase):
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
                    "This test creates a PDF with 5 pages, each page containing a Paragraph of text. Subsequent tests will check the way inline objects were persisted."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        N: int = 5
        for i in range(0, 5):
            layout.add(
                Paragraph(
                    "Page %d / %d" % (i + 1, N),
                    font_size=Decimal(20),
                    font_color=HexColor("f1cd2e"),
                )
            )
            for _ in range(0, 3):
                layout.add(
                    Paragraph(
                        """
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                        """,
                        font_size=Decimal(10),
                    )
                )
            if i != N - 1:
                page = Page()
                pdf.append_page(page)
                layout = SingleColumnLayout(page)

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_inline_object_io(self):

        bts: typing.Optional[bytes] = None
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            bts = in_file_handle.read()

        i: int = 0
        dictionary_nesting: int = 0
        while i < len(bts):

            # start of dictionary
            if bts[i] == ord("<") == bts[i + 1]:
                dictionary_nesting += 1
                i += 2
                continue

            # end of dictionary
            if bts[i] == ord(">") == bts[i + 1]:
                dictionary_nesting -= 1
                i += 2
                continue

            # inline array
            if dictionary_nesting > 0 and bts[i] == ord("["):
                while i < len(bts) and bts[i] != ord("]"):
                    i += 1
                assert bts[i] == ord("]")
                assert bts[i + 1] != ord("\n")

            # default
            i += 1
