import typing
import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import HexColor, FlexibleColumnWidthTable
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestAddAllEmoji(unittest.TestCase):
    """
    This test creates a PDF with an Image in it, this Image is a ScreenShot
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


    def test_write_document_with_one_emoji(self):

        for e in Emojis:

            # create empty document
            print("Writing PDF with Emojis.%s" % e.name)
            pdf: Document = Document()

            # create empty page
            page: Page = Page()

            # add page to document
            pdf.add_page(page)

            # add Image
            layout = SingleColumnLayout(page)
            layout.add(e.value)

            # write
            out_file = self.output_dir / "output_000.pdf"
            with open(out_file, "wb") as pdf_file_handle:
                PDF.dumps(pdf_file_handle, pdf)


    def test_write_document_with_all_emoji(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.add_page(page)

        # add Image
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with ALL Emoji in it"
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add image
        t: typing.Optional[Table] = None
        for i, e in enumerate(Emojis):
            if i % 200 == 0:
                if t is not None:
                    t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
                    t.no_borders()
                    layout.add(t)
                t = FlexibleColumnWidthTable(number_of_columns=20, number_of_rows=10, horizontal_alignment=Alignment.CENTERED)
            t.add(e.value)
        if t is not None:
            t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            t.no_borders()
            layout.add(t)

        # write
        out_file = self.output_dir / "output_001.pdf"
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare visually (there is no point whatsoever in doing this)
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)


if __name__ == "__main__":
    unittest.main()
