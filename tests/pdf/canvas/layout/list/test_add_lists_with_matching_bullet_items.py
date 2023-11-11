from decimal import Decimal

from borb.pdf import HexColor
from borb.pdf import UnorderedList
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.list.roman_numeral_ordered_list import (
    RomanNumeralOrderedList,
)
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddListWithMatchingBulletItems(TestCase):
    """
    This test creates a PDF with an ordered list in it.
    """

    def test_add_orderedlist_with_matching_bullet_items_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an ordered list in it. "
                "The elements in the list have varying font_size"
            )
        )
        layout.add(
            OrderedList()
            .add(
                Paragraph(
                    text="Lorem Ipsum Dolor Sit Amet Consectetur Nunc",
                    font_size=Decimal(12),
                )
            )
            .add(Paragraph(text="Ipsum", font_size=Decimal(14)))
            .add(Paragraph(text="Dolor", font_size=Decimal(16)))
            .add(Paragraph(text="Sit", font_size=Decimal(18)))
            .add(Paragraph(text="Amet", font_size=Decimal(20)))
        )
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_orderedlist_with_matching_bullet_items_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an ordered list in it. "
                "The elements in the list have varying font_color"
            )
        )
        layout.add(
            OrderedList()
            .add(
                Paragraph(
                    text="Lorem Ipsum Dolor Sit Amet Consectetur Nunc",
                    font_color=HexColor("a5ffd6"),
                )
            )
            .add(Paragraph(text="Ipsum", font_color=HexColor("56cbf9")))
            .add(Paragraph(text="Dolor", font_color=HexColor("0b3954")))
            .add(Paragraph(text="Sit", font_color=HexColor("f1cd2e")))
            .add(Paragraph(text="Amet", font_color=HexColor("de6449")))
        )
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_unorderedlist_with_matching_bullet_items_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an ordered list in it. "
                "The elements in the list have varying font_size"
            )
        )
        layout.add(
            UnorderedList()
            .add(
                Paragraph(
                    text="Lorem Ipsum Dolor Sit Amet Consectetur Nunc",
                    font_size=Decimal(12),
                )
            )
            .add(Paragraph(text="Ipsum", font_size=Decimal(14)))
            .add(Paragraph(text="Dolor", font_size=Decimal(16)))
            .add(Paragraph(text="Sit", font_size=Decimal(18)))
            .add(Paragraph(text="Amet", font_size=Decimal(20)))
        )
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_unorderedlist_with_matching_bullet_items_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an ordered list in it. "
                "The elements in the list have varying font_color"
            )
        )
        layout.add(
            UnorderedList()
            .add(
                Paragraph(
                    text="Lorem Ipsum Dolor Sit Amet Consectetur Nunc",
                    font_color=HexColor("a5ffd6"),
                )
            )
            .add(Paragraph(text="Ipsum", font_color=HexColor("56cbf9")))
            .add(Paragraph(text="Dolor", font_color=HexColor("0b3954")))
            .add(Paragraph(text="Sit", font_color=HexColor("f1cd2e")))
            .add(Paragraph(text="Amet", font_color=HexColor("de6449")))
        )
        with open(self.get_fourth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_romannumeralorderedList_with_matching_bullet_items_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an ordered list in it. "
                "The elements in the list have varying font_size"
            )
        )
        layout.add(
            RomanNumeralOrderedList()
            .add(
                Paragraph(
                    text="Lorem Ipsum Dolor Sit Amet Consectetur Nunc",
                    font_size=Decimal(12),
                )
            )
            .add(Paragraph(text="Ipsum", font_size=Decimal(14)))
            .add(Paragraph(text="Dolor", font_size=Decimal(16)))
            .add(Paragraph(text="Sit", font_size=Decimal(18)))
            .add(Paragraph(text="Amet", font_size=Decimal(20)))
        )
        with open(self.get_fifth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_romannumeralorderedList_with_matching_bullet_items_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an ordered list in it. "
                "The elements in the list have varying font_color"
            )
        )
        layout.add(
            RomanNumeralOrderedList()
            .add(
                Paragraph(
                    text="Lorem Ipsum Dolor Sit Amet Consectetur Nunc",
                    font_color=HexColor("a5ffd6"),
                )
            )
            .add(Paragraph(text="Ipsum", font_color=HexColor("56cbf9")))
            .add(Paragraph(text="Dolor", font_color=HexColor("0b3954")))
            .add(Paragraph(text="Sit", font_color=HexColor("f1cd2e")))
            .add(Paragraph(text="Amet", font_color=HexColor("de6449")))
        )
        with open(self.get_sixth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())
