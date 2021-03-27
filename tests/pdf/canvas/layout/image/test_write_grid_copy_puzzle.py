import logging
import unittest
from pathlib import Path

import requests
from PIL import Image as PILImage

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-grid-copy-puzzle.log"), level=logging.DEBUG
)


class TestWriteGridCopyPuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-grid-copy-puzzle")

    @staticmethod
    def _convert_png_to_jpg(image: PILImage.Image) -> PILImage.Image:

        # omit transparency
        fill_color = (255, 255, 255)  # new background color
        image_out = image.convert("RGBA")  # it had mode P after DL it from OP
        if image_out.mode in ("RGBA", "LA"):
            background = PILImage.new(image_out.mode[:-1], image_out.size, fill_color)
            background.paste(image_out, image_out.split()[-1])  # omit transparency
            image_out = background

        # convert to RGB
        image_out = image_out.convert("RGB")

        # return
        return image_out

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)

        # add title
        layout.add(
            Paragraph(
                "Copy the picture",
                font_size=Decimal(20),
                font_color=X11Color("YellowGreen"),
            )
        )

        layout.add(
            Paragraph(
                """
                Copy the picture using the grid lines as a guide. 
                You might find it easier to copy one square at a time. 
                Count the squares carefully!
                """,
                respect_newlines_in_text=True,
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        # add image
        image_a = PILImage.open(
            requests.get(
                "https://www.mozilla.org/media/protocol/img/logos/firefox/browser/logo-lg-high-res.fbc7ffbb50fd.png",
                stream=True,
            ).raw
        )
        image_a = TestWriteGridCopyPuzzle._convert_png_to_jpg(image_a)
        image_a = image_a.resize((256, 256))
        image_b = PILImage.new(size=(256, 256), color=(255, 255, 255), mode="RGB")
        pixels_a = image_a.load()
        pixels_b = image_b.load()
        for i in range(0, 256, 32):
            for j in range(0, 256):
                pixels_a[(i, j)] = (0, 0, 0)
                pixels_b[(i, j)] = (0, 0, 0)
                pixels_a[(j, i)] = (0, 0, 0)
                pixels_b[(j, i)] = (0, 0, 0)
        for j in range(0, 256):
            pixels_a[(255, j)] = (0, 0, 0)
            pixels_b[(255, j)] = (0, 0, 0)
            pixels_a[(j, 255)] = (0, 0, 0)
            pixels_b[(j, 255)] = (0, 0, 0)

        t: Table = Table(number_of_columns=2, number_of_rows=1)
        t.add(Image(image_a))
        t.add(Image(image_b))
        t.no_borders()
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout.add(t)

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
