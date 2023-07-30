import typing
import unittest
from decimal import Decimal

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestInlineObjectIO(TestCase):
    def test_write_document(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with 5 pages, each page containing a Paragraph of text. "
                "Subsequent tests will check the way inline objects were persisted."
            )
        )

        N: int = 5
        for i in range(0, 5):
            layout.add(
                Paragraph(
                    "Page %d / %d" % (i + 1, N),
                    font_size=Decimal(20),
                    font_color=HexColor("f1cd2e"),
                )
            )
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
                    )
                )
            if i != N - 1:
                page = Page()
                pdf.add_page(page)
                layout = SingleColumnLayout(page)

        # attempt to store PDF
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_inline_object_io(self):

        bts: typing.Optional[bytes] = None
        with open(self.get_first_output_file(), "rb") as in_file_handle:
            bts = in_file_handle.read()

        i: int = 0
        dictionary_nesting: int = 0
        while i < len(bts):

            # start of dictionary
            if bts[i] == ord("<") == bts[i + 1]:
                dictionary_nesting += 1
                i += 2
                continue

            # end of dictionary
            if bts[i] == ord(">") == bts[i + 1]:
                dictionary_nesting -= 1
                i += 2
                continue

            # inline array
            if dictionary_nesting > 0 and bts[i] == ord("["):
                while i < len(bts) and bts[i] != ord("]"):
                    i += 1
                assert bts[i] == ord("]")
                assert bts[i + 1] != ord("\n")

            # default
            i += 1
