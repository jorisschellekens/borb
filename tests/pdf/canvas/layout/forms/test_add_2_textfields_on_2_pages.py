import datetime
import unittest
from pathlib import Path

import typing

from borb.io.read.types import Decimal
from borb.pdf import Document, Page, SingleColumnLayout, PageLayout, PDF, FixedColumnWidthTable, Paragraph, HexColor
from borb.pdf.canvas.layout.forms.text_field import TextField
from tests.test_util import check_pdf_using_validator, compare_visually_to_ground_truth


class TestAdd2TextFieldsOn2Pages(unittest.TestCase):

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

    def test_add_two_textfields_on_two_pages(self):

        doc: Document = Document()

        # write TextField(s)
        for page_nr in range(0, 2):
            page: Page = Page()
            doc.add_page(page)
            layout: PageLayout = SingleColumnLayout(page)

            # write test info
            if page_nr == 0:
                layout.add(
                    FixedColumnWidthTable(
                        number_of_columns=2,
                        number_of_rows=3,
                        margin_top=Decimal(5),
                        margin_bottom=Decimal(5),
                    )
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
                    .add(Paragraph(
                        "This test creates a 2-page PDF, each Page containing a TextField"))
                    .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
                )

            # add TextField
            layout.add(TextField())

        # store
        out_file: Path = self.output_dir / "output.pdf"
        with open(out_file, "wb") as fh:
            PDF.dumps(fh, doc)

        # validate
        check_pdf_using_validator(out_file)
        compare_visually_to_ground_truth(out_file)