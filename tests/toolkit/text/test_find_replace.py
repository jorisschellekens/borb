import typing
import unittest
from decimal import Decimal

from borb.pdf import HexColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_find_replace import SimpleFindReplace
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestFindReplace(TestCase):
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
                "A subsequent test will attempt to extract all the text from this PDF."
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

    def test_find_replace_near_match(self):

        # create PDF
        self.test_create_dummy_pdf()

        # read PDF
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        assert doc is not None

        # find/replace
        doc = SimpleFindReplace.sub(
            pattern="elit", repl="oled", doc=doc, repl_font_size=Decimal(6.80)
        )

        # attempt to store PDF
        with open(self.get_second_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
        self.check_pdf_using_validator(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_find_replace_identical(self):

        # create PDF
        self.test_create_dummy_pdf()

        # read PDF
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        assert doc is not None

        # find/replace
        doc = SimpleFindReplace.sub(
            pattern="elit", repl="elit", doc=doc, repl_font_size=Decimal(6.5)
        )

        # attempt to store PDF
        with open(self.get_third_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
        self.check_pdf_using_validator(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file())

    def test_find_replace_near_match_different_color(self):

        # create PDF
        self.test_create_dummy_pdf()

        # read PDF
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        assert doc is not None

        # find/replace
        doc = SimpleFindReplace.sub(
            pattern="elit",
            repl="oled",
            doc=doc,
            repl_font_size=Decimal(6.80),
            repl_font_color=HexColor("ff0000"),
        )

        # attempt to store PDF
        with open(self.get_fourth_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
        self.check_pdf_using_validator(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())

    def test_find_replace_near_match_different_font(self):

        # create PDF
        self.test_create_dummy_pdf()

        # read PDF
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        assert doc is not None

        # find/replace
        doc = SimpleFindReplace.sub(
            "elit",
            "oled",
            doc,
            repl_font=StandardType1Font("Courier"),
            repl_font_size=Decimal(6.125),
        )

        # attempt to store PDF
        with open(self.get_fifth_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
        self.check_pdf_using_validator(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
