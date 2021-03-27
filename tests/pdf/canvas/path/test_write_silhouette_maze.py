import logging
import random
import typing
import unittest
from decimal import Decimal
from pathlib import Path

import requests
from PIL import Image as PILImage  # type: ignore [import]

from ptext.pdf.canvas.color.color import HexColor, X11Color
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.layout_element import Alignment
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.shape import DisjointShape
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir


class Maze:
    def __init__(self, width: int, height: int):
        assert width > 0
        assert height > 0
        self.width: int = width
        self.height: int = height
        self.cells = [
            [210 for _ in range(0, self.height)] for _ in range(0, self.width)
        ]
        self._build_maze()
        self._make_gap()
        self._make_gap(reverse_scan_order=True)

    def _unvisited_neighbours(self, x: int, y: int):
        nbs: typing.List[typing.Tuple[int, int]] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                # self is not a valid neighbour
                if i == 0 and j == 0:
                    continue
                if abs(i) == abs(j) == 1:
                    continue
                # check out-of-bounds
                if x + i >= self.width or x + i < 0:
                    continue
                if y + j >= self.height or y + j < 0:
                    continue
                if self.cells[x + i][y + j] == 210:
                    nbs.append((x + i, y + j))
        return nbs

    def get_walls(
        self, cell_size: int
    ) -> typing.List[
        typing.Tuple[typing.Tuple[Decimal, Decimal], typing.Tuple[Decimal, Decimal]]
    ]:
        walls: typing.List[
            typing.Tuple[typing.Tuple[Decimal, Decimal], typing.Tuple[Decimal, Decimal]]
        ] = []
        for i in range(0, self.width):
            for j in range(0, self.height):
                c = self.cells[i][j]
                if c % 2 == 0:
                    walls.append(
                        [
                            [i * cell_size, j * cell_size],
                            [(i + 1) * cell_size, j * cell_size],
                        ]
                    )
                if c % 3 == 0:
                    walls.append(
                        [
                            [(i + 1) * cell_size, j * cell_size],
                            [(i + 1) * cell_size, (j + 1) * cell_size],
                        ]
                    )
                if c % 5 == 0:
                    walls.append(
                        [
                            [i * cell_size, (j + 1) * cell_size],
                            [(i + 1) * cell_size, (j + 1) * cell_size],
                        ]
                    )
                if c % 7 == 0:
                    walls.append(
                        [
                            [i * cell_size, j * cell_size],
                            [i * cell_size, (j + 1) * cell_size],
                        ]
                    )
        return walls

    def _build_maze(self) -> None:

        # find first cell
        stk: typing.List[typing.Tuple[int, int]] = []
        for i in range(0, self.width):
            for j in range(0, self.height):
                if self.cells[i][j] == 210:
                    stk.append((i, j))
                    break
            if len(stk) > 0:
                break

        while len(stk) > 0:
            # pop a cell from the stack and make it the current cell
            current_cell: typing.Tuple[int, int] = stk[-1]
            stk.pop(-1)
            # If the current cell has any neighbours which have not been visited
            nbs = self._unvisited_neighbours(current_cell[0], current_cell[1])
            if len(nbs) > 0:
                # Push the current cell to the stack
                stk.append(current_cell)
                # Choose one of the unvisited neighbours
                nb = random.choice(nbs)
                # Remove the wall between the current cell and the chosen cell
                if current_cell[0] == nb[0]:
                    if current_cell[1] > nb[1]:
                        self.cells[current_cell[0]][current_cell[1]] /= 2
                        self.cells[nb[0]][nb[1]] /= 5
                    elif nb[1] > current_cell[1]:
                        self.cells[current_cell[0]][current_cell[1]] /= 5
                        self.cells[nb[0]][nb[1]] /= 2
                elif current_cell[1] == nb[1]:
                    if current_cell[0] > nb[0]:
                        self.cells[current_cell[0]][current_cell[1]] /= 7
                        self.cells[nb[0]][nb[1]] /= 3
                    elif nb[0] > current_cell[0]:
                        self.cells[current_cell[0]][current_cell[1]] /= 3
                        self.cells[nb[0]][nb[1]] /= 7
                # Mark the chosen cell as visited and push it to the stack
                stk.append((nb[0], nb[1]))

    def _make_gap(self, reverse_scan_order: bool = False):
        xs = (
            [x for x in reversed(range(0, self.width))]
            if reverse_scan_order
            else [x for x in range(0, self.width)]
        )
        ys = (
            [x for x in reversed(range(0, self.height))]
            if reverse_scan_order
            else [x for x in range(0, self.height)]
        )
        for i in xs:
            for j in ys:
                if i == 0 or i == self.width - 1 or j == 0 or j == self.height - 1:
                    if self.cells[i][j] != -1:
                        # mark as start
                        if i == 0:
                            self.cells[i][j] /= 7
                            return
                        if i == self.width - 1:
                            self.cells[i][j] /= 3
                            return
                        if j == 0:
                            self.cells[i][j] /= 2
                            return
                        if j == self.height - 1:
                            self.cells[i][j] /= 5
                            return
                elif self.cells[i][j] != -1 and (
                    self.cells[i - 1][j] == -1
                    or self.cells[i + 1][j] == -1
                    or self.cells[i][j - 1] == -1
                    or self.cells[i][j + 1] == -1
                ):
                    if self.cells[i - 1][j] == -1:
                        self.cells[i][j] /= 7
                        return
                    if self.cells[i + 1][j] == -1:
                        self.cells[i][j] /= 3
                        return
                    if self.cells[i][j - 1] == -1:
                        self.cells[i][j] /= 2
                        return
                    if self.cells[i][j + 1] == -1:
                        self.cells[i][j] /= 5
                        return


class SilhouetteMaze(Maze):
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

    def __init__(self, image: typing.Union[PILImage.Image, str]):
        if isinstance(image, str):
            image = PILImage.open(
                requests.get(
                    image,
                    stream=True,
                ).raw
            )
        assert isinstance(image, PILImage.Image)
        image = SilhouetteMaze._convert_png_to_jpg(image)
        if image.width * image.height > (128 * 128):
            scale = 128 / max(image.width, image.height)
            image = image.resize((int(image.width * scale), int(image.height * scale)))

        # basic rectangle
        self.width: int = image.width
        self.height: int = image.height
        self.cells = [
            [210 for _ in range(0, self.height)] for _ in range(0, self.width)
        ]
        # modify to match image
        remaining_pixels = self.width * self.height
        pixels = image.load()
        for i in range(0, self.width):
            for j in range(0, self.height):
                white_dist = self._dist(
                    pixels[(i, self.height - j - 1)], (255, 255, 255)
                )
                black_dist = self._dist(pixels[(i, self.height - j - 1)], (0, 0, 0))
                if white_dist < black_dist:
                    self.cells[i][j] = -1
                    remaining_pixels -= 1
        # call super to fill maze
        self._build_maze()
        self._make_gap()
        self._make_gap(reverse_scan_order=True)

    def _dist(self, t0, t1):
        return (t0[0] - t1[0]) ** 2 + (t0[1] - t1[1]) ** 2 + (t0[2] - t1[2]) ** 2


logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-silhouette-maze.log"), level=logging.DEBUG
)


class TestWriteMaze(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-silhouette-maze")

    def _write_maze_page(self, pdf: Document, maze_url: str, title_color: str):

        # add page
        page = Page()
        pdf.append_page(page)

        # generate maze
        m = SilhouetteMaze(maze_url)

        # add
        layout = SingleColumnLayout(page)

        # add title
        layout.add(
            Paragraph(
                "MAZE NR %d" % (page.get_page_info().get_page_number() + 1),
                font="TimesRoman",
                font_size=Decimal(20),
                font_color=HexColor(title_color),
            )
        )

        # add subtitle
        layout.add(
            Paragraph(
                """
                Can you solve this maze? 
                Try going from (lower) left to (upper) right.
                Good luck
                """,
                respect_newlines_in_text=True,
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        # add maze
        layout.add(
            DisjointShape(
                m.get_walls(Decimal(10)),
                stroke_color=HexColor(title_color),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            )
        )

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # fmt: off
        mazes = [
            ("https://i.pinimg.com/originals/1e/c2/a7/1ec2a73d0a45016c7d1b52ef9f11e740.png", "395E66"),
            ("https://i.pinimg.com/originals/f8/23/88/f823882e7c5fa42790e78f43ecf7e8bf.jpg", "387D7A"),
            ("https://i.pinimg.com/600x315/2d/94/33/2d94334b737efb5d3a5ef32aef9daefc.jpg", "32936F"),
            ("https://i.pinimg.com/originals/f1/c9/07/f1c907c09d65d5c86fba304fed1009ca.jpg", "26A96C"),
            ("https://cdn.pixabay.com/photo/2017/08/24/12/11/silhouette-2676573_960_720.png", "2BC016"),
            ("https://images-na.ssl-images-amazon.com/images/I/61bqYbAeUgL._AC_SL1500_.jpg", "395E66"),
            ("https://i.pinimg.com/originals/55/e8/91/55e891af7de086a8868e1a8e02fb4426.jpg","387D7A"),
            ("https://cdn.shopify.com/s/files/1/2123/8425/products/166422700-LRG_242a4c8b-cad5-476e-afd1-c8b882d48fc2_530x.jpg","32936F"),
            ("http://www.silhcdn.com/3/i/shapes/lg/7/6/d124067.jpg","26A96C"),
            ("https://cdn.pixabay.com/photo/2018/03/04/23/28/frog-3199601_1280.png","2BC016")
        ]
        # fmt: on

        # add mazes
        for (url, color) in mazes:
            for _ in range(0, 3):
                self._write_maze_page(pdf, url, color)

        # add ack page
        page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)

        # content of ack page
        layout.add(
            Paragraph(
                "Hi there,",
                font_color=HexColor("32936F"),
                font_size=Decimal(20),
            )
        )
        layout.add(
            Paragraph(
                "This PDF was made by pText. Check out the GitHub repository to find more fun examples of what you can do with PDF's.",
                font_color=X11Color("SlateGray"),
                font_size=Decimal(12),
            )
        )
        layout.add(
            Barcode(
                data="https://github.com/jorisschellekens/ptext-release",
                type=BarcodeType.QR,
                width=Decimal(64),
            )
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
