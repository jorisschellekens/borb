import logging
import unittest
from pathlib import Path

import requests
from PIL import Image as PILImage

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-table-with-image.log"), level=logging.DEBUG
)


class TestWriteTableWithImage(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-table-with-image")

    def _add_image_to_table(self, url: str, table: Table):
        im = PILImage.open(
            requests.get(
                url,
                stream=True,
            ).raw
        )
        table.add(
            Image(
                im,
                width=Decimal(128),
                height=Decimal(128),
                horizontal_alignment=Alignment.CENTERED,
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

        t = Table(number_of_rows=5, number_of_columns=3)
        t.add(Paragraph(" ", respect_spaces_in_text=True))
        t.add(
            Paragraph(
                "Close-up",
                font_color=X11Color("SteelBlue"),
                font_size=Decimal(20),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "Panoramic",
                font_color=X11Color("SteelBlue"),
                font_size=Decimal(20),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        t.add(Paragraph("Nature"))
        self._add_image_to_table(
            "https://images.unsplash.com/photo-1520860560195-0f14c411476e?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
            t,
        )
        self._add_image_to_table(
            "https://images.unsplash.com/photo-1613480123595-c5582aa551b9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
            t,
        )

        t.add(Paragraph("Architecture"))
        self._add_image_to_table(
            "https://images.unsplash.com/photo-1611321569296-1305a38ebd74?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
            t,
        )
        self._add_image_to_table(
            "https://images.unsplash.com/photo-1613262666714-acebcc37f11e?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
            t,
        )

        t.set_border_width_on_all_cells(Decimal(0.2))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout = SingleColumnLayout(page)
        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
