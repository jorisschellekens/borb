import unittest
import zlib
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout

from borb.io.read.types import Decimal as pDecimal
from borb.io.read.types import Dictionary, List, Name, Stream
from borb.pdf.canvas.color.color import X11Color
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from tests.test_util import compare_visually_to_ground_truth

unittest.TestLoader.sortTestMethodsUsing = None


class TestApplyRedactionAnnotations(unittest.TestCase):
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

    #
    #   the following tests use the "Tj"
    #

    def test_write_document_001(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and a Paragraph of text. "
                    "A subsequent test will add a redact annotation. The test after that applies the redaction annotations."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        layout.add(
            Paragraph(
                """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """,
                font_size=Decimal(10),
                vertical_alignment=Alignment.TOP,
                horizontal_alignment=Alignment.LEFT,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
        )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_add_redact_annotation_001(self):

        # attempt to read PDF
        doc = None
        l = RegularExpressionTextExtraction("[vV]eniam")
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

        for m in l.get_matches_for_page(0):
            for bb in m.get_bounding_boxes():
                bb = bb.grow(Decimal(2))
                doc.get_page(0).append_redact_annotation(
                    bb, stroke_color=X11Color("Black"), fill_color=X11Color("Black")
                )

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_apply_redact_annotation_001(self):

        with open(self.output_dir / "output_002.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        page: Page = doc.get_page(0)
        assert page is not None
        assert "Annots" in page
        assert isinstance(page["Annots"], List)
        assert len(page["Annots"]) == 1

        # apply redaction annotations
        doc.get_page(0).apply_redact_annotations()

        # attempt to store PDF
        with open(self.output_dir / "output_003.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_003.pdf")

    #
    #   the following tests use the "TJ" operator (rather than "Tj")
    #

    def test_write_document_002(self):

        pdf: Document = Document()

        page = Page()
        pdf.append_page(page)

        # create content stream
        content_stream = Stream()
        content_stream[
            Name("DecodedBytes")
        ] = b"""
            q
            BT
            /F1 10 Tf            
            59 640 Td            
            [(Lorem ipsum dolor sit amet,), 2, ( consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et)] TJ
            ET
            Q
        """
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Filter")] = Name("FlateDecode")
        content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))

        # set content of page
        page[Name("Contents")] = content_stream

        # set Font
        page[Name("Resources")] = Dictionary()
        page["Resources"][Name("Font")] = Dictionary()
        page["Resources"]["Font"][Name("F1")] = Dictionary()
        page["Resources"]["Font"]["F1"][Name("Type")] = Name("Font")
        page["Resources"]["Font"]["F1"][Name("Subtype")] = Name("Type1")
        page["Resources"]["Font"]["F1"][Name("Name")] = Name("F1")
        page["Resources"]["Font"]["F1"][Name("BaseFont")] = Name("Helvetica")
        page["Resources"]["Font"]["F1"][Name("Encoding")] = Name("MacRomanEncoding")

        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and a Paragraph of text. "
                    "A subsequent test will add a redact annotation. The test after that applies the redaction annotations."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # attempt to store PDF
        with open(self.output_dir / "output_004.pdf", "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

    def test_add_redact_annotation_002(self):

        # attempt to read PDF
        doc = None
        l = RegularExpressionTextExtraction("consectetur")
        with open(self.output_dir / "output_004.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

        for m in l.get_matches_for_page(0):
            for bb in m.get_bounding_boxes():
                bb = bb.grow(Decimal(2))
                doc.get_page(0).append_redact_annotation(
                    bb, stroke_color=X11Color("Black"), fill_color=X11Color("Black")
                )

        # attempt to store PDF
        with open(self.output_dir / "output_005.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_apply_redact_annotation_002(self):

        with open(self.output_dir / "output_005.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        page: Page = doc.get_page(0)
        assert page is not None
        assert "Annots" in page
        assert isinstance(page["Annots"], List)
        assert len(page["Annots"]) == 1

        # apply redaction annotations
        doc.get_page(0).apply_redact_annotations()

        # attempt to store PDF
        with open(self.output_dir / "output_006.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_006.pdf")
