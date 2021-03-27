import logging
import random
import time
import typing
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.list import UnorderedList
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-word-search.log"), level=logging.DEBUG
)


class WordSearch(Table):
    def __init__(self, words: typing.List[str]):

        # set solved grid to None
        self.solved_grid: typing.Optional[typing.List[typing.List[str]]] = None

        # call recursive algo to find grid
        w = max([len(x) for x in words])
        while self.solved_grid is None:

            # build empty grid
            g = [["." for _ in range(0, w)] for _ in range(0, w)]

            # recursion
            words = [x.upper() for x in words]
            random.shuffle(words)
            self._fit_words_in_grid(g, words)

            if self.solved_grid is None:
                w += 1

        # call constructor
        super(WordSearch, self).__init__(number_of_rows=w, number_of_columns=w)

        # add elements
        for i in range(0, len(self.solved_grid)):
            for j in range(0, len(self.solved_grid[i])):
                self.add(
                    Paragraph(
                        text=self.solved_grid[i][j],
                        horizontal_alignment=Alignment.CENTERED,
                    )
                )

        # no border
        self.no_borders()

    def _fit_words_in_grid(
        self,
        grid: typing.List[typing.List[str]],
        words_to_fit: typing.List[str],
        allow_reverse_horizontal: bool = True,
        allow_reverse_vertical: bool = True,
        allow_diagonal: bool = True,
        allow_reverse_diagonal=True,
        depth: int = 0,
        start_time: typing.Optional[float] = None,
        time_out: float = 10,
    ):

        # all words are already placed (in a previous iteration)
        if self.solved_grid is not None:
            return

        # taking too long
        if start_time is None:
            start_time = time.time()
        delta: float = abs(time.time() - start_time)
        if delta > time_out:
            return

        # all words are placed
        if len(words_to_fit) == 0:
            self.solved_grid = [
                [
                    random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") if y == "." else y
                    for y in x
                ]
                for x in grid
            ]
            return

        # attempt to fit next word
        if len(words_to_fit) > 0:

            # pop word
            w = words_to_fit[0]
            words_to_fit.pop(0)

            # attempt to fit word
            for i in range(0, len(grid)):
                for j in range(0, len(grid[i])):

                    ##
                    ## HORIZONTAL
                    ##

                    # out of bounds (horizontally)
                    grid_conflict = False
                    if j + len(w) > len(grid[i]):
                        grid_conflict = True

                    # check existing letters (horizontally)
                    if not grid_conflict:
                        for k in range(0, len(w)):
                            if grid[i][j + k] != "." and grid[i][j + k] != w[k]:
                                grid_conflict = True
                                break

                    # set (horizontally)
                    if not grid_conflict:
                        prev_vals: typing.List[str] = []
                        for k in range(0, len(w)):
                            prev_vals.append(grid[i][j + k])
                            grid[i][j + k] = w[k]

                        # recurse
                        self._fit_words_in_grid(
                            grid,
                            words_to_fit,
                            allow_reverse_horizontal,
                            allow_reverse_vertical,
                            allow_diagonal,
                            allow_reverse_diagonal,
                            depth + 1,
                            start_time,
                            time_out,
                        )

                        # unset
                        for k in range(0, len(w)):
                            grid[i][j + k] = prev_vals[k]

                    ##
                    ## VERTICAL
                    ##

                    # out of bounds (vertically)
                    grid_conflict = False
                    if i + len(w) > len(grid):
                        grid_conflict = True

                    # check existing letters
                    if not grid_conflict:
                        for k in range(0, len(w)):
                            if grid[i + k][j] != "." and grid[i + k][j] != w[k]:
                                grid_conflict = True
                                break

                    # set
                    if not grid_conflict:
                        prev_vals: typing.List[str] = []
                        for k in range(0, len(w)):
                            prev_vals.append(grid[i + k][j])
                            grid[i + k][j] = w[k]

                        # recurse
                        self._fit_words_in_grid(
                            grid,
                            words_to_fit,
                            allow_reverse_horizontal,
                            allow_reverse_vertical,
                            allow_diagonal,
                            allow_reverse_diagonal,
                            depth + 1,
                            start_time,
                            time_out,
                        )

                        # unset
                        for k in range(0, len(w)):
                            grid[i + k][j] = prev_vals[k]

                    ##
                    ## REVERSE VERTICAL
                    ##

                    r: float = depth / (depth + len(words_to_fit))
                    if allow_reverse_vertical and r > 0.75:

                        # out of bounds (inverse - vertically)
                        grid_conflict = False
                        if i + len(w) > len(grid):
                            grid_conflict = True

                        # check existing letters
                        if not grid_conflict:
                            for k in range(0, len(w)):
                                if (
                                    grid[i + k][j] != "."
                                    and grid[i + k][j] != w[len(w) - k - 1]
                                ):
                                    grid_conflict = True
                                    break

                        # set
                        if not grid_conflict:
                            prev_vals: typing.List[str] = []
                            for k in range(0, len(w)):
                                prev_vals.append(grid[i + k][j])
                                grid[i + k][j] = w[len(w) - k - 1]

                            # recurse
                            self._fit_words_in_grid(
                                grid,
                                words_to_fit,
                                allow_reverse_horizontal,
                                allow_reverse_vertical,
                                allow_diagonal,
                                allow_reverse_diagonal,
                                depth + 1,
                                start_time,
                                time_out,
                            )

                            # unset
                            for k in range(0, len(w)):
                                grid[i + k][j] = prev_vals[k]

                    ##
                    ## REVERSE HORIZONTAL
                    ##

                    if allow_reverse_horizontal and r > 0.75:

                        # out of bounds (horizontally)
                        grid_conflict = False
                        if j + len(w) > len(grid[i]):
                            grid_conflict = True

                        # check existing letters (reverse horizontally)
                        if not grid_conflict:
                            for k in range(0, len(w)):
                                if (
                                    grid[i][j + k] != "."
                                    and grid[i][j + k] != w[len(w) - k - 1]
                                ):
                                    grid_conflict = True
                                    break

                        # set (horizontally)
                        if not grid_conflict:
                            prev_vals: typing.List[str] = []
                            for k in range(0, len(w)):
                                prev_vals.append(grid[i][j + k])
                                grid[i][j + k] = w[len(w) - k - 1]

                            # recurse
                            self._fit_words_in_grid(
                                grid,
                                words_to_fit,
                                allow_reverse_horizontal,
                                allow_reverse_vertical,
                                allow_diagonal,
                                allow_reverse_diagonal,
                                depth + 1,
                                start_time,
                                time_out,
                            )

                            # unset
                            for k in range(0, len(w)):
                                grid[i][j + k] = prev_vals[k]

            # push word back
            words_to_fit.insert(0, w)


class TestWriteWordSearch(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-word-search")

    def test_write_document(self):

        words = [
            "COW",
            "PUPPY",
            "TURTLE",
            "PARROT",
            "SNAKE",
            "GOLDFISH",
            "HAMSTER",
            "KITTEN",
            "TURKEY",
            "DOVE",
            "HORSE",
            "BEE" "RABBIT",
            "DUCK",
            "SHRIMP",
            "PIG",
            "GOAT",
            "CRAB",
            "DOG",
            "DEER",
            "CAT",
            "MOUSE",
            "ELEPHANT",
            "LION",
            "PENGUIN",
            "SPARROW",
            "STORK",
            "HAWK",
        ]
        ws = WordSearch(words)

        pdf = Document()
        page = Page()
        pdf.append_page(page)

        # layout
        layout = MultiColumnLayout(page, number_of_columns=2)

        # add title
        layout.add(
            Paragraph(
                """
                A word search, word find, word seek, 
                word sleuth or mystery word puzzle is a word game that consists of the letters of words placed in a grid, 
                which usually has a rectangular or square shape.
                The objective of this puzzle is to find and mark all the words hidden inside the box.
                """,
                font_color=X11Color("SlateGray"),
            )
        )

        # add grid
        layout.add(ws)

        # go to next column
        layout.switch_to_next_column()

        # add title
        layout.add(
            Paragraph(
                "Word Search", font_size=Decimal(20), font_color=X11Color("YellowGreen")
            )
        )

        # add list
        ul = UnorderedList()
        for w in words:
            ul.add(Paragraph(w))
        layout.add(ul)

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
