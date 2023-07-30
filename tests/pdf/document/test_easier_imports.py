import unittest

# simplified imports
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestWriteHelloWorldWithEasierImports(TestCase):
    def test_write_hello_world_with_easier_imports(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.add_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # add a Paragraph object
        layout.add(Paragraph("Hello World!", font_color=HexColor("56cbf9")))

        # attempt to store PDF
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())
