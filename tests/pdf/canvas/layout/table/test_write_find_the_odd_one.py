import logging
import random
import typing
import unittest
from pathlib import Path

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
    filename=Path(get_log_dir(), "test-write-find-the-odd-one.log"), level=logging.DEBUG
)


class TestWriteFindTheOddOne(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-find-the-odd-one")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)

        # add title
        layout.add(
            Paragraph(
                "Match Up Puzzle",
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

        # random locations for each image
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
        random.shuffle(imgs)
        image_positions: typing.Dict[int, str] = {}
        for i, img_url in enumerate(imgs[0 : (N + 1)]):
            # place image 1
            p0 = random.randint(0, N ** 2)
            while p0 in image_positions:
                p0 = random.randint(0, N ** 2)
            image_positions[p0] = img_url
            if i != 0:
                # place image 2
                p1 = random.randint(0, N ** 2)
                while p1 in image_positions:
                    p1 = random.randint(0, N ** 2)
                image_positions[p1] = img_url

        t = Table(number_of_rows=N, number_of_columns=N)
        for i in range(0, N ** 2):
            if i in image_positions:
                t.add(Image(image_positions[i], width=Decimal(32), height=Decimal(32)))
            else:
                t.add(Paragraph(" ", respect_spaces_in_text=True))
        t.no_borders()
        t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
