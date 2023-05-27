from borb.pdf import ChunkOfText
from borb.pdf import Document
from borb.pdf import HeterogeneousParagraph
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from tests.test_case import TestCase


class TestAddHeterogeneousParagraphUsingAccentedCharacters(TestCase):
    def test_add_heterogeneousparagraph_using_accented_characters(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF."
            )
        )

        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Dirección"),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Código"),
                    Emojis.SMILE.value,
                    ChunkOfText("Número"),
                ]
            )
        )
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
