import unittest
from decimal import Decimal
from pathlib import Path

from borb.io.read.types import Dictionary
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.shape.shape import Shape
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestPageHasEmptyResourceDictionary(unittest.TestCase):
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

    def test_page_has_empty_resource_dictionary(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add Shape
        W: Decimal = page.get_page_info().get_width()
        H: Decimal = page.get_page_info().get_height()
        bottom_y: Decimal = H / Decimal(2) - Decimal(100)
        left_x: Decimal = W / Decimal(2) - Decimal(100)
        bounding_box: Rectangle = Rectangle(
            left_x, bottom_y, Decimal(200), Decimal(200)
        )
        Shape(
            LineArtFactory.regular_n_gon(bounding_box, 5),
            stroke_color=HexColor("56cbf9"),
            fill_color=HexColor("56cbf9"),
        ).layout(page, bounding_box)

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_001.pdf")

        # check Resources dictionary
        page_dictionary: Dictionary = pdf["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][0]
        assert page_dictionary is not None
        assert "Resources" in page_dictionary
