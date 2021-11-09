import unittest
from decimal import Decimal
from math import ceil
from pathlib import Path

from tests.test_util import compare_visually_to_ground_truth

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.free_space_finder import FreeSpaceFinder
from borb.pdf.pdf import PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestAddSquareAnnotationInFreeSpace(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_document_write_grid(self):

        # attempt to read PDF
        doc = None
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        l: FreeSpaceFinder = FreeSpaceFinder()
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

        # write (debug purposes)
        N: int = ceil(doc.get_page(0).get_page_info().get_width() / 10)
        M: int = ceil(doc.get_page(0).get_page_info().get_height() / 10)
        for i in range(0, M):
            print("adding annotations, row %d / %d" % (i + 1, M))
            for j in range(0, N):
                if l._grid_per_page[0]._availability[i][j]:
                    continue
                x = Decimal(i * 10)
                y = Decimal(j * 10)
                doc.get_page(0).append_square_annotation(
                    Rectangle(x, y, Decimal(10), Decimal(10)),
                    stroke_color=HexColor("BF4E30"),
                    fill_color=HexColor("BF4E30"),
                )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_document_write_annotation(self):

        # attempt to read PDF
        doc = None
        l: FreeSpaceFinder = FreeSpaceFinder()
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

        # ideal rectangle is somewhere in the middle of the Page
        w: Decimal = doc.get_page(0).get_page_info().get_width()
        h: Decimal = doc.get_page(0).get_page_info().get_height()
        ideal_rectangle: Rectangle = Rectangle(
            w / Decimal(2) - 50, h / Decimal(2) - 50, Decimal(100), Decimal(100)
        )

        free_rectangle = l.get_free_space_for_page(0, ideal_rectangle)

        # add annotation
        doc.get_page(0).append_square_annotation(
            free_rectangle,
            stroke_color=HexColor("0B3954"),
            fill_color=HexColor("f1cd2e"),
        )

        # attempt to store PDF
        output_path: Path = self.output_dir / "output_002.pdf"
        with open(output_path, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(output_path)
