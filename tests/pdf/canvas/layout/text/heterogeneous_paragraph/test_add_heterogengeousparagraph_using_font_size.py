from _decimal import Decimal

from borb.pdf import ChunkOfText
from borb.pdf import Document
from borb.pdf import HeterogeneousParagraph
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from tests.test_case import TestCase


class TestAddHeterogeneousParagraphUsingFontSize(TestCase):
    def test_add_heterogeneousparagraph_using_font_size_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with font_size 12"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", font_size=Decimal(12)),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", font_size=Decimal(12)),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", font_size=Decimal(12)),
                ]
            )
        )
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_heterogeneousparagraph_using_font_size_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with font_size 14"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", font_size=Decimal(14)),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", font_size=Decimal(14)),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", font_size=Decimal(14)),
                ]
            )
        )
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_heterogeneousparagraph_using_font_size_003(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with font_size 16"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", font_size=Decimal(16)),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", font_size=Decimal(16)),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", font_size=Decimal(16)),
                ]
            )
        )
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_heterogeneousparagraph_using_font_size_004(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with font_size 18"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", font_size=Decimal(18)),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", font_size=Decimal(18)),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", font_size=Decimal(18)),
                ]
            )
        )
        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_heterogeneousparagraph_using_font_size_005(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a HeterogeneousParagraph to the PDF with font_size 20"
            )
        )
        layout.add(
            HeterogeneousParagraph(
                chunks_of_text=[
                    ChunkOfText("Lorem", font_size=Decimal(20)),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("Ipsum", font_size=Decimal(20)),
                    Emojis.SMILE.value,
                    ChunkOfText("Dolor", font_size=Decimal(20)),
                ]
            )
        )
        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())
