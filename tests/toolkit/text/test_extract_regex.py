import typing
import unittest
from decimal import Decimal

from borb.pdf import ConnectedShape
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractRegularExpression(TestCase):
    def test_create_dummy_pdf(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an empty Page, and a Paragraph of text. "
                "A subsequent test will attempt to match a regular expression against the lipsum text."
            )
        )

        layout.add(
            Paragraph(
                """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """,
                font_size=Decimal(10),
                vertical_alignment=Alignment.TOP,
                horizontal_alignment=Alignment.LEFT,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
        )

        # attempt to store PDF
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_match_regular_expression(self):

        # attempt to read PDF
        doc: typing.Optional[Document] = None
        l = RegularExpressionTextExtraction("ad minim veniam")
        with open(self.get_first_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

        assert doc is not None

        bb = l.get_matches()[0][0].get_bounding_boxes()[0]
        assert 196 <= int(bb.x) <= 198
        assert 615 <= int(bb.y) <= 617
        assert 74 <= int(bb.width) <= 76
        assert 6 <= int(bb.height) <= 8

        bb = bb.grow(Decimal(2))
        ConnectedShape(
            LineArtFactory.rectangle(bb),
            stroke_color=HexColor("DE6449"),
            fill_color=None,
        ).paint(doc.get_page(0), bb)

        # attempt to store PDF
        with open(self.get_second_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())


if __name__ == "__main__":
    unittest.main()
