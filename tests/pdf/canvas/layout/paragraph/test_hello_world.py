import unittest
from pathlib import Path

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestWriteHelloWorld(unittest.TestCase):
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
        pdf.append_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # add a Paragraph object
        layout.add(Paragraph("Hello World!"))

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
