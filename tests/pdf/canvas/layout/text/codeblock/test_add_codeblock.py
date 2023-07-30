from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.codeblock import CodeBlock
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddCodeblock(TestCase):
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
                test_description="This test creates a PDF with a CodeBlock in it."
            )
        )

        # read self
        with open(__file__, "r") as self_file_handle:
            file_contents = self_file_handle.read()
        layout.add(
            CodeBlock(
                file_contents,
                font_size=Decimal(5),
            )
        )

        # store
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())
