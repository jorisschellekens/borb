import typing
import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import check_pdf_using_validator

unittest.TestLoader.sortTestMethodsUsing = None


class TestDocumentFileSize(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

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

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        check_pdf_using_validator(out_file)

    def test_check_file_size_001(self):

        # determine input location
        out_file = self.output_dir / "output.pdf"

        # read
        with open(out_file, "rb") as pdf_file_handle:
            document = PDF.loads(pdf_file_handle)

        # check file_size
        s: typing.Optional[Decimal] = document.get_document_info().get_file_size()
        assert s is not None
        assert 1000 <= s <= 1100

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
