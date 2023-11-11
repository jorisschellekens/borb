import typing
import unittest

from borb.io.read.types import Decimal
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddEmoji(TestCase):
    """
    This test creates a PDF with an Image in it, this Image is a ScreenShot
    """

    def test_add_single_emoji_001(self):

        # create empty document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add Emoji
        layout.add(
            self.get_test_header(
                f"This test writes a PDF containing a single emoji, {Emojis.SMILE.name}. It does so for every emoji."
            )
        )
        layout.add(Emojis.SMILE.value)

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_add_single_emoji(self):

        for e in Emojis:

            # debug
            print("Writing PDF with Emojis.%s" % e.name)

            # create empty document
            pdf: Document = Document()
            page: Page = Page()
            pdf.add_page(page)
            layout = SingleColumnLayout(page)

            # add Emoji
            layout.add(
                self.get_test_header(
                    f"This test writes a PDF containing a single emoji, {e.name.replace('_', ' ')}. It does so for every emoji."
                )
            )
            layout.add(e.value)

            # write
            with open(self.get_first_output_file(), "wb") as pdf_file_handle:
                PDF.dumps(pdf_file_handle, pdf)

    def test_add_all_emoji(self):

        # create empty document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header(
                "This tests creates a PDF with all available emoji in it."
            )
        )

        # add image
        t: typing.Optional[Table] = None
        for i, e in enumerate(Emojis):
            if i % 200 == 0:
                if t is not None:
                    t.set_padding_on_all_cells(
                        Decimal(2), Decimal(2), Decimal(2), Decimal(2)
                    )
                    t.no_borders()
                    layout.add(t)
                t = FlexibleColumnWidthTable(
                    number_of_columns=20,
                    number_of_rows=10,
                    horizontal_alignment=Alignment.CENTERED,
                )
            t.add(e.value)
        if t is not None:
            t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            t.no_borders()
            layout.add(t)

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_3_emoji(self):

        # create empty document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(self.get_test_header("This tests creates a PDF with 3 emoji in it."))

        # add emoji
        layout.add(Emojis.A.value)
        layout.add(Emojis.AB.value)
        layout.add(Emojis.ABC.value)

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_emoji_to_heterogeneousparagraph(self):
        pass


if __name__ == "__main__":
    unittest.main()
