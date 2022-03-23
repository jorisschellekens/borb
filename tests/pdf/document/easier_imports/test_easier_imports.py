import unittest
from pathlib import Path

# simplified imports
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF


unittest.TestLoader.sortTestMethodsUsing = None


class TestWriteHelloWorldWithEasierImports(unittest.TestCase):
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

    def test_write_hello_world_with_easier_imports(self):

        # create an empty Document
        pdf = Document()

        # add an empty Page
        page = Page()
        pdf.append_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = SingleColumnLayout(page)

        # add a Paragraph object
        layout.add(Paragraph("Hello World!", font_color=HexColor("56cbf9")))

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
