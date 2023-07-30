import typing
import unittest
from decimal import Decimal

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestDocumentFileSize(TestCase):
    def test_write_hello_world(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.add_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # add a Paragraph object
        layout.add(Paragraph("Hello World!"))

        # attempt to store PDF
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_check_file_size_001(self):

        # read
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            document = PDF.loads(pdf_file_handle)

        # check file_size
        s: typing.Optional[Decimal] = document.get_document_info().get_file_size()
        assert s is not None
        assert 1000 <= s <= 1200

    def test_check_file_size_002(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.add_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # add a Paragraph object
        layout.add(Paragraph("Hello World!"))

        # check file_size
        s: typing.Optional[Decimal] = pdf.get_document_info().get_file_size()
        assert s is None
