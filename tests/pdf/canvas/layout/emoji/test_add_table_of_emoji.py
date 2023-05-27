from borb.pdf import Document
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from tests.test_case import TestCase


class TestAddListOfEmoji(TestCase):
    def test_add_table_of_emoji(self):

        # create empty document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        layout.add(
            self.get_test_header(
                "This test adds an FlexibleColumnWidthTable to a PDF containing Emoji."
            )
        )
        layout.add(
            FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3)
            .add(Emojis.SMILEY.value)
            .add(Emojis.OCTOCAT.value)
            .add(Emojis.APPLE.value)
            .add(Emojis.OCTOCAT.value)
            .add(Emojis.APPLE.value)
            .add(Emojis.SMILEY.value)
            .add(Emojis.APPLE.value)
            .add(Emojis.SMILEY.value)
            .add(Emojis.OCTOCAT.value)
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
