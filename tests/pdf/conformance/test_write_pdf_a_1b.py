import unittest
from pathlib import Path

from borb.io.read.types import Dictionary, Name, String
from borb.io.write.conformance_level import ConformanceLevel
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWritePDFA1B(unittest.TestCase):
    """
    This test creates a PDF with a few PDF graphics in it
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

    def test_write_pdf_a_1b(self):

        # create empty Document
        pdf = Document()

        # create empty Page
        page = Page()

        # add Page to Document
        pdf.append_page(page)

        # create PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        # add Paragraph
        layout.add(Paragraph("Hello World!"))

        info_dictionary: Dictionary = Dictionary()
        info_dictionary[Name("Title")] = String("Title Value")
        info_dictionary[Name("Subject")] = String("Subject Value")
        info_dictionary[Name("Creator")] = String("Creator Value")
        info_dictionary[Name("Author")] = String("Author Value")
        info_dictionary[Name("Keywords")] = String("Keyword1 Keyword2 Keyword3")
        pdf["XRef"]["Trailer"][Name("Info")] = info_dictionary

        # attempt to store PDF
        out_file = self.output_dir / "output_001.pdf"
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf, ConformanceLevel.PDFA_1B)

    def test_re_open_pdfa_1_b(self):

        # attempt to re-open PDF
        out_file = self.output_dir / "output_001.pdf"
        with open(out_file, "rb") as in_file_handle:
            pdf = PDF.loads(in_file_handle)

        # assert XMP meta data
        xmp = pdf.get_xmp_document_info()
        assert xmp.get_title() == "Title Value"
        assert xmp.get_creator() == "Creator Value"
        assert xmp.get_author() == "Author Value"
        assert xmp.get_subject() == "Subject Value"
        assert xmp.get_keywords() == "Keyword1 Keyword2 Keyword3"

    def test_re_save_pdf_a_1_b(self):

        # attempt to re-open PDF
        out_file = self.output_dir / "output_001.pdf"
        with open(out_file, "rb") as in_file_handle:
            pdf = PDF.loads(in_file_handle)

        # attempt to store PDF
        out_file = self.output_dir / "output_002.pdf"
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf, ConformanceLevel.PDFA_1B)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            pdf = PDF.loads(in_file_handle)

        # assert XMP meta data
        xmp = pdf.get_xmp_document_info()
        assert xmp.get_title() == "Title Value"
        assert xmp.get_creator() == "Creator Value"
        assert xmp.get_author() == "Author Value"
        assert xmp.get_subject() == "Subject Value"
        assert xmp.get_keywords() == "Keyword1 Keyword2 Keyword3"

        compare_visually_to_ground_truth(out_file)
