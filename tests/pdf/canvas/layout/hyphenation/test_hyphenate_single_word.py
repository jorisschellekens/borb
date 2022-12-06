import datetime
import unittest
from pathlib import Path

from borb.pdf import Document, FixedColumnWidthTable, SingleColumnLayout, PageLayout
from borb.pdf import Page
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation
from borb.pdf import Alignment
from borb.pdf import Paragraph
from borb.pdf import PDF
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf import HexColor

from decimal import Decimal

from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestAddHyphenatedParagraph(unittest.TestCase):
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

    def test_hyphenate_single_word(self):

        # create Document
        doc: Document = Document()

        # create Page
        page: Page = Page()
        doc.add_page(page)

        # set PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        # add test information
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an single hyphenated word in it. This previously crashed the layout algorithm in Paragraph."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        r: Rectangle = Rectangle(
            Decimal(59.5),
            Decimal(550),
            Decimal(50),
            Decimal(70),
        )

        Paragraph(
            "Alignment",
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            text_alignment=Alignment.CENTERED,
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            border_color=HexColor("ff0000"),
            hyphenation=Hyphenation("en-us"),
        ).paint(page, r)

        # store
        out_file = self.output_dir / "output.pdf"
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
