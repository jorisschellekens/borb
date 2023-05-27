import typing
from decimal import Decimal

from borb.io.read.types import Dictionary
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestPageHasEmptyResourceDictionary(TestCase):
    def test_create_dummy_pdf(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add Shape
        W: Decimal = page.get_page_info().get_width()
        H: Decimal = page.get_page_info().get_height()
        bottom_y: Decimal = H / Decimal(2) - Decimal(100)
        left_x: Decimal = W / Decimal(2) - Decimal(100)
        bounding_box: Rectangle = Rectangle(
            left_x, bottom_y, Decimal(200), Decimal(200)
        )
        ConnectedShape(
            LineArtFactory.regular_n_gon(bounding_box, 5),
            stroke_color=HexColor("56cbf9"),
            fill_color=HexColor("56cbf9"),
        ).paint(page, bounding_box)

        # attempt to store PDF
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_resource_dictionary_is_empty(self):

        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as fh:
            doc = PDF.loads(fh)

        assert doc is not None

        # check Resources dictionary
        page_dictionary: Dictionary = doc["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][0]
        assert page_dictionary is not None
        assert "Resources" in page_dictionary
