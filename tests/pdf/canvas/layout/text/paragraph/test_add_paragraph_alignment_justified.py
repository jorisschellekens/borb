import random

from borb.pdf import PDF
from borb.pdf import Alignment
from borb.pdf import Lipsum
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import Page
from borb.pdf import Document

from tests.test_case import TestCase


class TestAddParagraphAlignmentJustified(TestCase):
    def test_add_paragraph_alignment_justified(self):

        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a Paragraph to the PDF. The Paragraph is aligned JUSTIFIED."
            )
        )

        # mult-line paragraph
        random.seed(0)
        layout.add(
            Paragraph(
                Lipsum.generate_lipsum_text(5), text_alignment=Alignment.JUSTIFIED
            )
        )

        # single-line paragraph
        layout.add(
            Paragraph(
                Lipsum.generate_lipsum_text(1), text_alignment=Alignment.JUSTIFIED
            )
        )

        # store
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)

        # compare
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
