import json
import typing
import unittest
from decimal import Decimal

from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestAddEmbeddedFile(TestCase):
    """
    This test creates a PDF with a Paragraph object in it.
    An embedded file will later be added to this PDF.
    """

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
                test_description="This test creates a PDF with a Paragraph object in it. "
                "An embedded file will later be added to this PDF."
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

        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_append_binary_file(self):

        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        assert doc is not None
        doc.add_embedded_file(
            "embedded_data.json",
            json.dumps(
                {
                    "Name": "Schellekens",
                    "Firstname": "Joris",
                    "Github": "https://www.github.com/jorisschellekens",
                }
            ).encode("latin1"),
        )

        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_extract_embedded_file(self):
        doc: typing.Optional[Document] = None
        with open(self.get_second_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)
        assert doc is not None

        embeded_file_as_dictionary = json.loads(
            doc.get_embedded_file("embedded_data.json")
        )

        #             "Name": "Schellekens",
        #             "Firstname": "Joris",
        #             "Github": "https://www.github.com/jorisschellekens",
        assert embeded_file_as_dictionary["Name"] == "Schellekens"
        assert embeded_file_as_dictionary["Firstname"] == "Joris"
        assert (
            embeded_file_as_dictionary["Github"]
            == "https://www.github.com/jorisschellekens"
        )
