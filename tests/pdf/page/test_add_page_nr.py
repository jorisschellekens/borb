import random
from _decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.geometry.rectangle import Rectangle
from tests.test_case import TestCase


class TestAddPageNr(TestCase):
    def test_add_page_nr(self):

        doc: Document = Document()

        # seed random
        random.seed(1024)

        # add initial Page
        p: Page = Page()
        doc.add_page(p)

        # PageLayout
        layout: PageLayout = SingleColumnLayout(p)

        # add content
        for _ in range(0, 20):
            layout.add(Paragraph(Lipsum.generate_lipsum_text(5)))

        # get the number of pages
        number_of_pages: int = int(doc.get_document_info().get_number_of_pages())

        # iterate over each Page
        for page_nr in range(0, number_of_pages):
            page: Page = doc.get_page(page_nr)

            # add page nr
            # do this in the utmost right corner
            Paragraph(
                f"page {page_nr+1} out of {number_of_pages}",
                horizontal_alignment=Alignment.RIGHT,
                vertical_alignment=Alignment.BOTTOM,
            ).paint(
                page,
                Rectangle(
                    page.get_page_info().get_width() - Decimal(100),
                    Decimal(0),
                    Decimal(100),
                    Decimal(20),
                ),
            )

        # save
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
