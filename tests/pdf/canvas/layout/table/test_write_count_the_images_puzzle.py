import logging
import random
import typing
import unittest
from math import sqrt
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-count-the-images-puzzle.log"),
    level=logging.DEBUG,
)


class TestWriteCountTheImagesPuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-count-the-images-puzzle")

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
                "Count The Pictures Puzzle",
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

        N = 32
        w = int(sqrt(N) + 2)
        random.shuffle(imgs)
        image_positions: typing.Dict[int, str] = {}
        images_used = []
        for i in [random.randint(0, len(imgs)) for _ in range(0, N)]:
            i = (i + len(imgs)) % len(imgs)
            # place image
            p0 = random.randint(0, w ** 2)
            while p0 in image_positions:
                p0 = random.randint(0, N ** 2)
            url = imgs[i]
            if url not in images_used:
                images_used.append(url)
            image_positions[p0] = url

        t = Table(number_of_rows=w, number_of_columns=w)
        for i in range(0, w ** 2):
            if i in image_positions:
                t.add(Image(image_positions[i], width=Decimal(32), height=Decimal(32)))
            else:
                t.add(Paragraph(" ", respect_spaces_in_text=True))
        t.no_borders()
        t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        layout.add(t)

        # write count table
        for _ in range(0, 5):
            layout.add(Paragraph(" ", respect_spaces_in_text=True))

        t2 = Table(number_of_rows=1, number_of_columns=len(images_used) * 2)
        for url in images_used:
            t2.add(
                TableCell(
                    Image(url, width=Decimal(16), height=Decimal(15)),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            t2.add(Paragraph(" ", respect_spaces_in_text=True))
        t2.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        layout.add(t2)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
