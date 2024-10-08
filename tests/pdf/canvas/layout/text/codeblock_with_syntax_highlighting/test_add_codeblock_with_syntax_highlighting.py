from borb.io.read.types import Decimal
from borb.pdf import CodeBlockWithSyntaxHighlighting
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddCodeblockWithSyntaxHighlighting(TestCase):
    """
    This test creates a PDF with a CodeBlock element in it.
    """

    def test_add_codeblock(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a CodeBlockWithSyntaxHighlighting in it."
            )
        )

        # read self
        with open(__file__, "r") as self_file_handle:
            file_contents = self_file_handle.read()
        layout.add(
            CodeBlockWithSyntaxHighlighting(
                file_contents,
                font_size=Decimal(6),
            )
        )

        # store
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())
