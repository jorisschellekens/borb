import logging
import random
import typing
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
    filename=Path(get_log_dir(), "test-write-mystery-picture-puzzle.log"),
    level=logging.DEBUG,
)


class TestWriteMysteryPicturePuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-mystery-picture-puzzle")

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

    def _split_picture_to_grid(self, url: str) -> typing.List[Image]:
        image = PILImage.open(
            requests.get(
                url,
                stream=True,
            ).raw
        )
        image = self._convert_png_to_jpg(image)
        image = image.resize((256, 256))
        image_pixels = image.load()
        blocks = [
            PILImage.new(mode="RGB", size=(64, 64), color=(255, 255, 255))
            for x in range(0, 16)
        ]
        for k in range(0, 16):
            r = k % 4
            c = int(k / 4)
            block_pixels = blocks[k].load()
            for i in range(0, 64):
                for j in range(0, 64):
                    if i == 0 or j == 0 or i == 63 or j == 63:
                        block_pixels[(i, j)] = (0, 0, 0)
                    else:
                        block_pixels[(i, j)] = image_pixels[(r * 64 + i, c * 64 + j)]
        return blocks

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

        pics: typing.List[Image] = self._split_picture_to_grid(
            "https://icons.iconarchive.com/icons/iconka/meow-2/128/cat-sing-icon.png"
        )
        # fmt: off
        coords: typing.List[str] = [
            "1A", "2A", "3A", "4A",
            "1B", "2B", "3B", "4B",
            "1C", "2C", "3C", "4C",
            "1D", "2D", "3D", "4D",
        ]
        # fmt: on
        pics_and_coords = [x for x in zip(pics, coords)]
        random.shuffle(pics_and_coords)

        t = Table(
            number_of_rows=4,
            number_of_columns=8,
            column_widths=[
                Decimal(1),
                Decimal(3),
                Decimal(1),
                Decimal(3),
                Decimal(1),
                Decimal(3),
                Decimal(1),
                Decimal(3),
            ],
        )
        for p, c in pics_and_coords:
            t.add(Paragraph(c, font_size=Decimal(6)))
            t.add(Image(p))

        t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        t.no_borders()
        layout.add(t)

        # table 2
        t2 = Table(number_of_columns=4, number_of_rows=4)
        for c in coords:
            t2.add(
                Paragraph(
                    "\n" + c + "\n",
                    respect_newlines_in_text=True,
                    font_color=X11Color("LightGray"),
                    horizontal_alignment=Alignment.CENTERED,
                )
            )
        t2.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        layout.add(t2)

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
