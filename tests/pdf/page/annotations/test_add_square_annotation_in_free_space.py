import unittest
from decimal import Decimal
from pathlib import Path

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
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # determine free space
        space_finder = FreeSpaceFinder(doc.get_page(0))

        # write (debug purposes)
        for i in range(0, space_finder.get_number_of_rows_in_grid()):
            print(
                "adding annotations, row %d / %d"
                % (i + 1, space_finder.get_number_of_rows_in_grid())
            )
            for j in range(0, space_finder.get_number_of_columns_in_grid()):
                if space_finder._grid[i][j]:
                    continue
                w = Decimal(space_finder.get_grid_resolution())
                x = Decimal(i) * w
                y = Decimal(j) * w
                doc.get_page(0).append_square_annotation(
                    Rectangle(x, y, w, w),
                    stroke_color=HexColor("72A276"),
                    fill_color=HexColor("72A276"),
                )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_document_write_annotation(self):

        # attempt to read PDF
        doc = None
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # determine free space
        space_finder = FreeSpaceFinder(doc.get_page(0))

        w: Decimal = doc.get_page(0).get_page_info().get_width()
        h: Decimal = doc.get_page(0).get_page_info().get_height()
        ideal_rectangle: Rectangle = Rectangle(
            w / Decimal(2) - 50, h / Decimal(2) - 50, Decimal(100), Decimal(100)
        )

        free_rectangle = space_finder.find_free_space(ideal_rectangle)

        # add annotation
        doc.get_page(0).append_square_annotation(
            free_rectangle, stroke_color=HexColor("86CD82")
        )

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
