from borb.pdf import ChunkOfText
from borb.pdf import Document
from borb.pdf import HeterogeneousParagraph
from borb.pdf import HexColor
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from tests.test_case import TestCase


class TestAddHeterogeneousParagraphUsingBackgroundColor(TestCase):
    def test_add_heterogeneousparagraph_using_background_color_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with background_color 12"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", background_color=HexColor("023047")),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", background_color=HexColor("023047")),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", background_color=HexColor("023047")),
                ]
            )
        )
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_heterogeneousparagraph_using_background_color_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with background_color 14"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", background_color=HexColor("FFB703")),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", background_color=HexColor("FFB703")),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", background_color=HexColor("FFB703")),
                ]
            )
        )
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_heterogeneousparagraph_using_background_color_003(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with background_color 16"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", background_color=HexColor("FB8500")),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", background_color=HexColor("FB8500")),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", background_color=HexColor("FB8500")),
                ]
            )
        )
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_heterogeneousparagraph_using_background_color_004(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with background_color 18"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", background_color=HexColor("219EBC")),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", background_color=HexColor("219EBC")),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", background_color=HexColor("219EBC")),
                ]
            )
        )
        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_heterogeneousparagraph_using_background_color_005(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with background_color 20"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", background_color=HexColor("8ECAE6")),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", background_color=HexColor("8ECAE6")),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", background_color=HexColor("8ECAE6")),
                ]
            )
        )
        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())
