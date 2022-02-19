import datetime
import typing
import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.remote_go_to_annotation import (
    RemoteGoToAnnotation,
)
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth

unittest.TestLoader.sortTestMethodsUsing = None


class TestAddRemoteGoToAnnotation(unittest.TestCase):
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

    def test_add_remote_go_to_annotation(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and a remote-go-to annotation"
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add annotation
        w: Decimal = pdf.get_page(0).get_page_info().get_width()
        h: Decimal = pdf.get_page(0).get_page_info().get_height()
        r = Rectangle(
            w / Decimal(2) - Decimal(32),
            h / Decimal(2) - Decimal(32),
            Decimal(64),
            Decimal(64),
        )

        Paragraph("borbpdf.com", font_color=HexColor("004573")).layout(
            pdf.get_page(0), r
        )

        pdf.get_page(0).append_annotation(
            RemoteGoToAnnotation(bounding_box=r, uri="https://www.borbpdf.com")
        )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # attempt to re-open PDF
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_001.pdf")

    def test_add_remote_go_to_annotation_by_regex(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and a remote-go-to annotation"
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add text
        chunks: typing.List[ChunkOfText] = [
            ChunkOfText(x)
            for x in ["Click", " here", " to", " visit", " borbpdf.com", "!"]
        ]
        chunks[4]._font_color = HexColor("004573")
        hp: HeterogeneousParagraph = HeterogeneousParagraph(chunks)
        layout.add(hp)

        # add annotation
        pdf.get_page(0).append_annotation(
            RemoteGoToAnnotation(
                bounding_box=chunks[4].get_bounding_box(), uri="https://www.borbpdf.com"
            )
        )

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # attempt to re-open PDF
        with open(self.output_dir / "output_002.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")
