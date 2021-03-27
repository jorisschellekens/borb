import logging
import random
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
    filename=Path(get_log_dir(), "test-write-match-the-shadow-puzzle.log"),
    level=logging.DEBUG,
)


class TestMatchTheShadowPuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-match-the-shadow-puzzle")

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

    @staticmethod
    def _make_image_shadow(url: str):
        image = PILImage.open(
            requests.get(
                url,
                stream=True,
            ).raw
        )
        # convert
        image = TestMatchTheShadowPuzzle._convert_png_to_jpg(image)
        # blackify
        pixels = image.load()
        for i in range(0, image.width):
            for j in range(0, image.height):
                r, g, b = pixels[(i, j)]
                g = int((r + g + b) / 3)
                pixels[(i, j)] = (g, g, g)

        # return
        return image

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create empty document
        pdf: Document = Document()
        page: Page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)

        # add title
        layout.add(
            Paragraph(
                "Match The Shadow",
                font_size=Decimal(20),
                font_color=X11Color("YellowGreen"),
            )
        )

        # add explanation
        layout.add(
            Paragraph(
                """
                These simple "match up" puzzles help children with observation skills. 
                They will also need to learn a way of marking or remembering which items they have matched, 
                so that they can identify the odd ones out. 
                If you would like to reuse puzzles you could place counters on each "pair" that your child finds, perhaps.""",
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        # add image
        imgs = [
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Orc-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/King-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Knight-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Medusa-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Monster-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Sorceress-Witch-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Centaur-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Elf-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Poison-Spider-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Unicorn-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Viking-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Villager-icon.png",
            "https://icons.iconarchive.com/icons/chanut/role-playing/128/Dragon-Egg-icon.png",
        ]
        N = 10
        imgs = imgs[0:N]
        random.shuffle(imgs)

        shadows = [TestMatchTheShadowPuzzle._make_image_shadow(x) for x in imgs]
        random.shuffle(imgs)

        t = Table(number_of_columns=5, number_of_rows=N)
        for i in range(0, N):
            t.add(Image(imgs[i], width=Decimal(32), height=Decimal(32)))
            t.add(Paragraph(" ", respect_spaces_in_text=True))
            t.add(Paragraph(" ", respect_spaces_in_text=True))
            t.add(Paragraph(" ", respect_spaces_in_text=True))
            t.add(Image(shadows[i], width=Decimal(32), height=Decimal(32)))
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
