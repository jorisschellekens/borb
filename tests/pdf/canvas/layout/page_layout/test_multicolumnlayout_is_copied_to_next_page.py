import random
from decimal import Decimal

from borb.pdf import Lipsum
from borb.pdf import MultiColumnLayout
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import ThreeColumnLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import TwoColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestMultiColumnLayoutIsCopiedToNextPage(TestCase):
    """
    This test creates a PDF with multiple pages.
    """

    def test_multicolumnlayout_is_copied_to_next_page_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 1 column"
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 16)
        ]:
            layout.add(Paragraph(s))
        pdf.pop_page(0)
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_multicolumnlayout_is_copied_to_next_page_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = TwoColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 2 column",
                font_size=Decimal(8),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 16)
        ]:
            layout.add(Paragraph(s, font_size=Decimal(10)))
        pdf.pop_page(0)
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_multicolumnlayout_is_copied_to_next_page_003(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = ThreeColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 3 columns",
                font_size=Decimal(6),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 16)
        ]:
            layout.add(Paragraph(s, font_size=Decimal(8)))
        pdf.pop_page(0)
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())
