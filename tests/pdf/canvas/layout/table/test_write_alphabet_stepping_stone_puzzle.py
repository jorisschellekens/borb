import copy
import math
import random
import typing
import unittest
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_output_dir


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return (self.x * 32) + (self.y * 97)

    def __eq__(self, other):
        return isinstance(other, Point) and other.x == self.x and other.y == self.y

    def __str__(self):
        return "{%d, %d}" % (self.x, self.y)

    def __deepcopy__(self, memodict={}):
        return Point(self.x, self.y)


class SteppingStonePuzzle(Table):
    def __init__(
        self,
        desired_sequence: typing.List[str],
        random_elements: typing.List[str],
        start_image: str,
        end_image: str,
    ):
        self.accepted_path = None

        # build grid
        d = int(math.sqrt(len(desired_sequence)) + 3)
        self._generate_grid(
            accepted_starts=[Point(2, 0), Point(2, 1), Point(0, 2), Point(1, 2)],
            accepted_ends=[
                Point(d - 1, d - 3),
                Point(d - 2, d - 3),
                Point(d - 3, d - 1),
                Point(d - 3, d - 2),
            ],
            forbidden=[
                Point(0, 0),
                Point(1, 0),
                Point(0, 1),
                Point(1, 1),
                Point(d - 2, d - 2),
                Point(d - 2, d - 1),
                Point(d - 1, d - 2),
                Point(d - 1, d - 1),
            ],
            path=[],
            desired_path_length=len(desired_sequence),
            bound=d,
        )

        # build table
        super(SteppingStonePuzzle, self).__init__(number_of_columns=d, number_of_rows=d)

        # set cells
        for i in range(0, d):
            for j in range(0, d):
                if i == j == 0:
                    self.add(
                        TableCell(
                            Image(start_image, width=Decimal(32), height=Decimal(32)),
                            row_span=2,
                            col_span=2,
                        )
                    )
                    continue
                if i <= 1 and j <= 1:
                    continue
                if i == j == d - 2:
                    self.add(
                        TableCell(
                            Image(end_image, width=Decimal(32), height=Decimal(32)),
                            row_span=2,
                            col_span=2,
                        )
                    )
                    continue
                if i >= d - 2 and j >= d - 2:
                    continue
                if Point(i, j) in self.accepted_path:
                    index = self.accepted_path.index(Point(i, j))
                    self.add(
                        Paragraph(
                            desired_sequence[index],
                            horizontal_alignment=Alignment.CENTERED,
                        )
                    )
                else:
                    self.add(
                        Paragraph(
                            random.choice(random_elements),
                            horizontal_alignment=Alignment.CENTERED,
                        )
                    )

        # no border
        self.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        self.no_borders()

    def _generate_grid(
        self,
        accepted_starts: typing.List[Point],
        accepted_ends: typing.List[Point],
        forbidden: typing.List[Point],
        path: typing.List[Point],
        desired_path_length: int,
        bound: int,
    ):

        # path found
        if self.accepted_path is not None:
            return

        # end
        if len(path) == desired_path_length:
            if path[-1] in accepted_ends:
                self.accepted_path = copy.deepcopy(path)
            return

        # init
        if len(path) == 0:
            for p in accepted_starts:
                path.append(p)
                self._generate_grid(
                    accepted_starts,
                    accepted_ends,
                    forbidden,
                    path,
                    desired_path_length,
                    bound,
                )
                path.remove(p)

        # build
        if len(path) > 0:
            last_point = path[-1]
            nbs = [
                Point(last_point.x, last_point.y - 1),
                Point(last_point.x, last_point.y + 1),
                Point(last_point.x - 1, last_point.y),
                Point(last_point.x + 1, last_point.y),
            ]

            # filter out out-of-bounds
            nbs = [
                p for p in nbs if p.x >= 0 and p.x < bound and p.y >= 0 and p.y < bound
            ]

            # filter forbidden
            nbs = [p for p in nbs if p not in forbidden]

            # filter out duplicates
            nbs = [p for p in nbs if p not in path]

            # shuffle
            random.shuffle(nbs)

            for p in nbs:
                path.append(p)
                self._generate_grid(
                    accepted_starts,
                    accepted_ends,
                    forbidden,
                    path,
                    desired_path_length,
                    bound,
                )
                path.remove(p)


class WriteAlphabetSteppingStonePuzzle(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-write-alphabet-stepping-stone-puzzle"
        )

    def test_write_document(self):

        pdf = Document()
        page = Page()
        pdf.append_page(page)

        # layout
        layout = MultiColumnLayout(page, number_of_columns=2)

        #
        # add title
        layout.add(
            Paragraph(
                """
                Help the person find their way home by colouring in a path through the stepping stones by making a sentence.  
                A really fun way to practice the alphabet!
                """,
                font_color=X11Color("SlateGray"),
                font_size=Decimal(8),
            )
        )

        seq = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        layout.add(
            SteppingStonePuzzle(
                seq,
                seq,
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/King-icon.png",
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/Castle-icon.png",
            )
        )

        # go to next column
        layout.switch_to_next_column()

        # add title
        layout.add(
            Paragraph(
                "Stepping Stones",
                font_size=Decimal(20),
                font_color=X11Color("YellowGreen"),
            )
        )

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
