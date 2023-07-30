import unittest
from decimal import Decimal

from borb.pdf.canvas.layout.annotation.link_annotation import DestinationType
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestAddOutline(TestCase):
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
                test_description="This test creates a PDF with several Paragraph object in it."
                "A series of outlines will later be added to this PDF."
            )
        )

        for _ in range(0, 5):
            page = Page()
            pdf.add_page(page)
            layout = SingleColumnLayout(page)
            for _ in range(0, 3):
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
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # check
        self.check_pdf_using_validator(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_outline(self):

        with open(self.get_first_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        # fmt: off
        doc.add_outline("Lorem", 0, page_nr=0, destination_type=DestinationType.FIT)
        doc.add_outline("Ipsum", 0, page_nr=1, destination_type=DestinationType.FIT)
        doc.add_outline("Dolor", 1, page_nr=0, destination_type=DestinationType.FIT)
        doc.add_outline("Sit", 2, page_nr=1, destination_type=DestinationType.FIT)
        doc.add_outline("Amet", 3, page_nr=0, destination_type=DestinationType.FIT)
        doc.add_outline("Consectetur", 3, page_nr=1, destination_type=DestinationType.FIT)
        doc.add_outline("Adipiscing", 3, page_nr=0, destination_type=DestinationType.FIT)
        doc.add_outline("Elit", 1, page_nr=1, destination_type=DestinationType.FIT)
        # fmt: on

        # attempt to store PDF
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)

        # check
        self.check_pdf_using_validator(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_outline_exists(self):

        with open(self.get_second_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        assert int(doc["XRef"]["Trailer"]["Root"]["Outlines"]["Count"]) == 8
