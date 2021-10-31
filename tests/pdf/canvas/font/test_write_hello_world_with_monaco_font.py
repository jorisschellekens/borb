import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteHelloWorldWithMonacoFont(unittest.TestCase):
    """
    This test loads a truetype _font from a .ttf file and attempts to use it to write 2 paragraphs of lorem ipsum.
    """

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

    def test_write_document_001(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # layout
        layout: PageLayout = SingleColumnLayout(page)

        # path to _font
        font_path: Path = Path(__file__).parent / "Monaco-Regular.ttf"
        assert font_path.exists()

        # add paragraph 1
        layout.add(
            Paragraph(
                "Hello World!",
                font=TrueTypeFont.true_type_font_from_file(font_path),
                font_size=Decimal(14),
            )
        )

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        compare_visually_to_ground_truth(out_file)
