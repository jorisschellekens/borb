import logging
import random
import typing
import unittest
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import HexColor
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


logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-square-maze.log"), level=logging.DEBUG
)


class TestWriteMaze(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-square-maze")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # generate maze
        m = Maze(20, 20)

        # add
        layout = SingleColumnLayout(page)

        # add title
        layout.add(
            Paragraph(
                "Square Maze",
                font_size=Decimal(20),
                font_color=HexColor("274029"),
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
            )
        )

        # add maze
        layout.add(
            DisjointShape(
                m.get_walls(Decimal(10)),
                stroke_color=HexColor("315C2B"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            )
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
