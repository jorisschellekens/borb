import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout, SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Alignment,
    Paragraph,
)
from ptext.pdf.canvas.layout.shape import Shape
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-dragon-curve.log"), level=logging.DEBUG
)


class TestWriteDragonCurve(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-dragon-curve")

    def _write_background(self, page: Page):
        layout = SingleColumnLayout(page)
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height()
        assert w is not None
        assert h is not None
        layout.add(
            Shape(
                LineArtFactory.dragon_curve(
                    bounding_box=Rectangle(Decimal(0), Decimal(0), w, h),
                    number_of_iterations=10,
                ),
                stroke_color=HexColor("64B6AC"),
                line_width=Decimal(1),
                fill_color=None,
            )
        )

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # background
        self._write_background(page)

        # foreground
        layout = MultiColumnLayout(page, number_of_columns=2)
        layout.add(
            Paragraph(
                "New shapes in LineArtFactory..",
                font_color=HexColor("EE964B"),
                font_size=Decimal(20),
            )
        )
        layout.switch_to_next_column()
        for _ in range(0, 11):
            layout.add(Paragraph(" ", respect_spaces_in_text=True))
        layout.add(
            Paragraph(
                "such as this cool dragon curve!",
                font_color=HexColor("F95738"),
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        Barcode(
            data="https://github.com/jorisschellekens/ptext-release",
            type=BarcodeType.QR,
            stroke_color=HexColor("64B6AC"),
            width=Decimal(128),
        ).layout(
            page,
            Rectangle(
                page.get_page_info().get_width() - Decimal(200),
                Decimal(100),
                Decimal(256),
                Decimal(256),
            ),
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
