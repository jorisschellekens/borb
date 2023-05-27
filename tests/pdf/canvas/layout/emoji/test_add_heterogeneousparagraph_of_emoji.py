from borb.pdf import ChunkOfText
from borb.pdf import Document
from borb.pdf import HeterogeneousParagraph
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from tests.test_case import TestCase


class TestAddHeterogeneousParagraphOfEmoji(TestCase):
    def test_add_heterogeneousparagraph_of_emoji(self):

        # create empty document
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        layout.add(
            self.get_test_header(
                "This test adds a HeterogengeousParagraph to a PDF containing Emoji."
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem Ipsum "),
                    Emojis.OCTOCAT.value,
                    ChunkOfText(" Dolor Sit"),
                    ChunkOfText(" Amet"),
                ]
            )
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
