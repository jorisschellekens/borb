import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.io.read.types import Name, List
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


class TestCopyCircleAnnotation(unittest.TestCase):
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

    def test_create_document_001(self):

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
                    "This test creates a PDF with an empty Page, and a circle annotation."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add annotation
        w: Decimal = pdf.get_page(0).get_page_info().get_width()
        h: Decimal = pdf.get_page(0).get_page_info().get_height()
        pdf.get_page(0).append_annotation(
            CircleAnnotation(
                bounding_box=Rectangle(
                    w / Decimal(2) - Decimal(32),
                    h / Decimal(2) - Decimal(32),
                    Decimal(64),
                    Decimal(64),
                ),
                stroke_color=HexColor("0B3954"),
                fill_color=HexColor("f1cd2e"),
            )
        )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # test
        compare_visually_to_ground_truth(self.output_dir / "output_001.pdf")

    def test_create_document_002(self):
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
                    "This test creates an empty PDF. A later test will copy an annotation (from another document) to it."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # test
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")

    def test_copy_circle_annotation(self):

        # open document 1
        doc_in_a = None
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            doc_in_a = PDF.loads(in_file_handle)

        # open document 2
        doc_in_b = None
        with open(self.output_dir / "output_002.pdf", "rb") as in_file_handle:
            doc_in_b = PDF.loads(in_file_handle)

        # copy annotations
        annots = doc_in_a.get_page(0).get_annotations()
        doc_in_b.get_page(0)[Name("Annots")] = List()
        for a in annots:
            doc_in_b.get_page(0)["Annots"].append(a)

        # attempt to store PDF
        with open(self.output_dir / "output_003.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc_in_b)

        # test
        compare_visually_to_ground_truth(self.output_dir / "output_003.pdf")
