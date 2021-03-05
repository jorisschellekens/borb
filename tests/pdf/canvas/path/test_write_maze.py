import logging
import random
import typing
import unittest
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import HexColor, X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout, MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.shape import DisjointShape, Shape
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class Maze:
    def __init__(self, width: int, height: int):
        assert width > 0
        assert height > 0
        self.width: int = width
        self.height: int = height
        self.cells = [
            [210 for _ in range(0, self.height)] for _ in range(0, self.height)
        ]
        self._build_maze()

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
        stk: typing.List[typing.Tuple[int, int]] = [(0, 0)]
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


logging.basicConfig(filename="../../../logs/test-write-maze.log", level=logging.DEBUG)


class TestWriteMaze(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../output/test-write-maze")

    def _write_maze_page(
        self, pdf: Document, maze_width: int = 64, maze_height: int = 64
    ):

        # add page
        page = Page()
        pdf.append_page(page)

        # generate maze
        m = Maze(maze_width, maze_height)

        layout = SingleColumnLayout(page)

        # add title
        layout.add(
            Paragraph(
                "MAZE %d" % page.get_page_info().get_page_number(),
                font="TimesRoman",
                font_size=Decimal(20),
                font_color=HexColor("D72638"),
            )
        )

        # add subtitle
        layout.add(
            Paragraph(
                """
                Can you solve the maze? 
                Go from the upper-left corner to the bottom-right
                """,
                respect_newlines_in_text=True,
            )
        )

        # add maze
        layout.add(
            DisjointShape(
                m.get_walls(Decimal(10)),
                stroke_color=HexColor("140F2D"),
                line_width=Decimal(2),
            )
        )

        # add footer art
        Shape(
            LineArtFactory.rectangle(
                bounding_box=Rectangle(0, 0, page.get_page_info().get_width(), 10)
            ),
            stroke_color=HexColor("D72638"),
            fill_color=HexColor("D72638"),
        ).layout(
            page, bounding_box=Rectangle(0, 32, page.get_page_info().get_width(), 100)
        )
        Shape(
            LineArtFactory.rectangle(
                bounding_box=Rectangle(0, 0, page.get_page_info().get_width(), 2)
            ),
            stroke_color=HexColor("140F2D"),
            fill_color=HexColor("140F2D"),
        ).layout(
            page, bounding_box=Rectangle(0, 20, page.get_page_info().get_width(), 100)
        )

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        for i in range(0, 32):
            print("generating 16 x 16 maze %d / 32" % (i + 1))
            self._write_maze_page(pdf, 16, 16)

        for i in range(0, 32):
            print("generating 32 x 32 maze %d / 32" % (i + 1))
            self._write_maze_page(pdf, 32, 32)

        for i in range(0, 32):
            print("generating 64 x 64 maze %d / 32" % (i + 1))
            self._write_maze_page(pdf, 64, 64)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
