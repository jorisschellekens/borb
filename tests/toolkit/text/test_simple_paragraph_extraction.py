import typing
import unittest

from borb.io.read.types import Decimal
from borb.pdf import ConnectedShape
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_paragraph_extraction import SimpleParagraphExtraction
from tests.test_case import TestCase


class TestSimpleParagraphExtraction(TestCase):
    """
    This test creates a PDF with an unsplash Image in it
    """

    def test_create_dummy_pdf(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.add_page(page)

        # add Image
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a Paragraph in it."
            )
        )

        layout.add(
            Paragraph(
                """
        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, 
        eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. 
        Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, 
        sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. 
        Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
        sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
        Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? 
        Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, 
        vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
        """,
                font_size=Decimal(8),
            )
        )

        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_simple_paragraph_extraction(self):

        # read document
        l: SimpleParagraphExtraction = SimpleParagraphExtraction(
            maximum_multiplied_leading=Decimal(1.7)
        )
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l])

        assert doc is not None

        # add SquareAnnotation(s)
        for p in l.get_paragraphs()[0]:
            ConnectedShape(
                LineArtFactory.rectangle(p.get_previous_layout_box()),
                stroke_color=HexColor("f1cd2e"),
                fill_color=None,
            ).paint(doc.get_page(0), p.get_previous_layout_box())

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())


if __name__ == "__main__":
    unittest.main()
