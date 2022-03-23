import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.circle_annotation import CircleAnnotation
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestAddCircleAnnotation(unittest.TestCase):
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

    def test_add_circle_annotations(self):

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
                    "This test creates a PDF with an empty Page, and nine circle annotations"
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add annotation
        w: Decimal = pdf.get_page(0).get_page_info().get_width()
        h: Decimal = pdf.get_page(0).get_page_info().get_height()
        for i in range(0, 3):
            for j in range(0, 3):
                pdf.get_page(0).append_annotation(
                    CircleAnnotation(
                        bounding_box=Rectangle(
                            w / Decimal(2) - Decimal(32 * 1.5) + i * 32,
                            h / Decimal(2) - Decimal(32 * 1.5) + j * 32,
                            Decimal(32),
                            Decimal(32),
                        ),
                        stroke_color=HexColor("0B3954"),
                        fill_color=HexColor("f1cd2e"),
                    )
                )

        # attempt to store PDF
        with open(self.output_dir / "output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # attempt to re-open PDF
        with open(self.output_dir / "output.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf")

    def test_annotation_names(self):

        # attempt to re-open PDF
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # check whether a Document was loaded
        assert doc is not None

        # check names
        annots = doc["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][0]["Annots"]
        assert str(annots[0]["NM"]) == "annotation-000"
        assert str(annots[1]["NM"]) == "annotation-001"
        assert str(annots[2]["NM"]) == "annotation-002"
        assert str(annots[3]["NM"]) == "annotation-003"
        assert str(annots[4]["NM"]) == "annotation-004"
        assert str(annots[5]["NM"]) == "annotation-005"
        assert str(annots[6]["NM"]) == "annotation-006"
        assert str(annots[7]["NM"]) == "annotation-007"
        assert str(annots[8]["NM"]) == "annotation-008"
