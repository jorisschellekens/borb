import logging
import typing
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-nonogram.log"), level=logging.DEBUG
)

import requests
from PIL import Image as PILImage  # type: ignore [import]


class Nonogram(Table):
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

    def __init__(self, image: typing.Union[str, PILImage.Image]):
        if isinstance(image, str):
            image = PILImage.open(
                requests.get(
                    image,
                    stream=True,
                ).raw
            )
        assert isinstance(image, PILImage.Image)

        # include solution
        self.include_solution = False

        # convert to RGB
        image = Nonogram._convert_png_to_jpg(image)

        # scale if needed
        if image.width * image.height > (20 * 20):
            scale = 20 / max(image.width, image.height)
            image = image.resize((int(image.width * scale), int(image.height * scale)))

        clues_horizontal = [[0] for _ in range(0, image.height)]
        clues_vertical = [[0] for _ in range(0, image.width)]
        pixels = image.load()
        for i in range(0, image.height):
            for j in range(0, image.width):
                white_dist = self._dist(pixels[(j, i)], (255, 255, 255))
                black_dist = self._dist(pixels[(j, i)], (0, 0, 0))
                if black_dist < white_dist:
                    clues_horizontal[i][-1] += 1
                else:
                    if clues_horizontal[i][-1] != 0:
                        clues_horizontal[i].append(0)

        solution = [
            [False for _ in range(0, image.width + 1)]
            for _ in range(0, image.height + 1)
        ]
        for i in range(0, image.width):
            for j in range(0, image.height):
                white_dist = self._dist(pixels[(i, j)], (255, 255, 255))
                black_dist = self._dist(pixels[(i, j)], (0, 0, 0))
                if black_dist < white_dist:
                    clues_vertical[i][-1] += 1
                    solution[j][i] = True
                else:
                    if clues_vertical[i][-1] != 0:
                        clues_vertical[i].append(0)

        clues_horizontal = [
            x if x[-1] != 0 or len(x) == 1 else x[:-1] for x in clues_horizontal
        ]
        clues_vertical = [
            x if x[-1] != 0 or len(x) == 1 else x[:-1] for x in clues_vertical
        ]

        super(Nonogram, self).__init__(
            number_of_columns=image.width + 1,
            number_of_rows=image.height + 1,
            column_widths=[
                Decimal(5) if x == 0 else Decimal(1) for x in range(0, image.width + 1)
            ],
        )
        self.add(
            TableCell(
                Paragraph(" ", respect_spaces_in_text=True),
                border_top=False,
                border_left=False,
            )
        )
        for c in clues_vertical:
            txt = "".join([str(x) + "\n" for x in c])[:-1]
            self.add(
                TableCell(
                    Paragraph(
                        txt,
                        font_size=Decimal(4),
                        horizontal_alignment=Alignment.CENTERED,
                        respect_newlines_in_text=True,
                    ),
                    padding_top=Decimal(2),
                    padding_bottom=Decimal(2),
                )
            )

        # add clues
        for i, c in enumerate(clues_horizontal):
            txt = "".join([str(x) + " " for x in c])[:-1]
            self.add(
                TableCell(
                    Paragraph(
                        txt,
                        horizontal_alignment=Alignment.CENTERED,
                        font_size=Decimal(4),
                    ),
                    padding_top=Decimal(2),
                    padding_bottom=Decimal(5),
                )
            )
            for j in range(0, image.width):
                if solution[i][j] and self.include_solution:
                    self.add(
                        TableCell(Paragraph("X"), background_color=X11Color("Black"))
                    )
                else:
                    self.add(Paragraph(""))

        # set border width
        self.set_border_width_on_all_cells(Decimal(0.2))

    def _dist(self, t0, t1):
        return (t0[0] - t1[0]) ** 2 + (t0[1] - t1[1]) ** 2 + (t0[2] - t1[2]) ** 2


class TestWriteNonogram(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-nonogram")

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

        # write title
        layout.add(
            Paragraph(
                "Nonogram", font_size=Decimal(20), font_color=X11Color("YellowGreen")
            )
        )

        # write text
        layout.add(
            Paragraph(
                """
            Nonograms, also known as Paint by Numbers, Picross, Griddlers, Pic-a-Pix, and various other names, 
            are picture logic puzzles in which cells in a grid must be colored or left blank according to numbers 
            at the side of the grid to reveal a hidden picture. 
            In this puzzle type, the numbers are a form of discrete tomography that measures how many 
            unbroken lines of filled-in squares there are in any given row or column. 
            For example, a clue of "4 8 3" would mean there are sets of four, eight, and three filled squares, 
            in that order, with at least one blank square between successive sets.
            """,
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        # write nonogram
        ng = Nonogram(
            # "https://i.pinimg.com/originals/f8/23/88/f823882e7c5fa42790e78f43ecf7e8bf.jpg"
            "https://cdn.shopify.com/s/files/1/2123/8425/products/166422700-LRG_242a4c8b-cad5-476e-afd1-c8b882d48fc2_530x.jpg"
        )
        layout.add(ng)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
