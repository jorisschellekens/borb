import typing
import unittest
from decimal import Decimal

from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.font_extraction import FontExtraction
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractFontNames(TestCase):
    """
    This test creates a PDF with 3 paragraphs of text in it, each in a different (standard 14) _font.
    """

    def test_create_dummy_pdf(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # layout
        layout: PageLayout = SingleColumnLayout(page)

        # add test information
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with 3 paragraphs of text in it, "
                "each in a different (standard 14) _font."
            )
        )

        fonts: typing.List[str] = ["Helvetica", "Courier", "Times-Roman"]

        # add paragraph 1
        for font_name in fonts:
            layout.add(
                Paragraph(
                    """
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                    """,
                    font=font_name,
                    font_size=Decimal(12),
                )
            )

        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_extract_font_names(self):

        # extract _font names
        font_names = []
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            l = FontExtraction()
            doc = PDF.loads(pdf_file_handle, [l])
            for fn in l.get_font_names()[0]:
                font_names.append(str(fn))

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # layout
        layout: PageLayout = SingleColumnLayout(page)

        # add test information
        layout.add(
            self.get_test_header(
                test_description="This test reads an existing PDF, "
                "and extracts the names of the fonts in the PDF."
            )
        )

        ul: UnorderedList = UnorderedList()
        for font_name in font_names:
            ul.add(Paragraph(font_name))
        layout.add(ul)

        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())
