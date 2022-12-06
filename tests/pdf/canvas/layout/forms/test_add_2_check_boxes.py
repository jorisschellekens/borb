import datetime
import typing
import unittest
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    PageLayout,
    PDF,
    FixedColumnWidthTable,
    Paragraph,
    HexColor,
)
from borb.pdf.canvas.layout.forms.check_box import CheckBox
from tests.test_util import check_pdf_using_validator, compare_visually_to_ground_truth


class TestAdd2Checkboxes(unittest.TestCase):
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

    def test_add_2_checkboxes(self):

        doc: Document = Document()

        # create empty page
        page: Page = Page()
        doc.add_page(page)

        layout: PageLayout = SingleColumnLayout(page)
        # fmt: off
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), font_color=HexColor("00ff00")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with 2 CheckBox objects in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        # fmt: on

        # add Checkboxes
        n: int = 2
        t: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_columns=2, number_of_rows=n, padding_top=Decimal(12)
        )
        for i in range(1, n + 1):
            t.add(Paragraph("CheckBox Nr. %d" % i))
            t.add(CheckBox())
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        layout.add(t)

        # write
        out_file = self.output_dir / "output.pdf"
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # check
        check_pdf_using_validator(out_file)
        compare_visually_to_ground_truth(out_file)

    def test_names_of_checkboxes(self):

        # read
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # assert we have read something
        assert doc is not None

        # assert on length
        fields = doc["XRef"]["Trailer"]["Root"]["AcroForm"]["Fields"]
        assert len(fields) == 2

        # assert on names
        assert fields[0]["T"] == "field-000"
        assert fields[1]["T"] == "field-001"
