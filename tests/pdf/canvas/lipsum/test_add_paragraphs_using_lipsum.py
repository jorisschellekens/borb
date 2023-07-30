import random

from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.lipsum.lipsum import Lipsum
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddParagraphsUsingLipsum(TestCase):
    def test_add_paragraphs_in_lipsum_style(self):

        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # content
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with dummy text in it."
            )
        )
        random.seed(2048)
        for s in [
            Lipsum.generate_lipsum_text(random.choice([5, 6, 7])) for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))

        # write
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # compare visually
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_paragraphs_in_agatha_christie_style(self):

        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # content
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with dummy text in it."
            )
        )
        random.seed(2048)
        for s in [
            Lipsum.generate_agatha_christie_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))

        # write
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # compare visually
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_paragraphs_in_aa_milne_style(self):
        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # content
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with dummy text in it."
            )
        )
        random.seed(2048)
        for s in [
            Lipsum.generate_alan_alexander_milne_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))

        # write
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # compare visually
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_paragraphs_in_arthur_conan_doyle_style(self):
        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # content
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with dummy text in it."
            )
        )
        random.seed(2048)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))

        # write
        with open(self.get_fourth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # compare visually
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_paragraphs_in_emily_bronte_style(self):
        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # content
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with dummy text in it."
            )
        )
        random.seed(2048)
        for s in [
            Lipsum.generate_emily_bronte_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))

        # write
        with open(self.get_fifth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # compare visually
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())
