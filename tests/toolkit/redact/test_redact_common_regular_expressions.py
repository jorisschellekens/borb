import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.io.read.types import List
from borb.pdf.canvas.color.color import X11Color
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.redact.common_regular_expressions import CommonRegularExpression
from borb.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)

unittest.TestLoader.sortTestMethodsUsing = None


class TestRedactCommonRegularExpressions(unittest.TestCase):
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
                    "This test creates a PDF with a table of (commonly deemed) sensitive information, such as social security number, email, etc. "
                    "A subsequent test will then look for those patterns and redact them."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        layout.add(
            Table(number_of_rows=5, number_of_columns=2, margin_top=Decimal(12))
            # heading
            .add(Paragraph("Information Type", font="Helvetica-Bold"))
            .add(Paragraph("Example", font="Helvetica-Bold"))
            # row 1
            .add(Paragraph("Email"))
            .add(Paragraph("joris.schellekens.1989@gmail.com"))
            # row 2
            .add(Paragraph("Telephone"))
            .add(Paragraph("+32 53 79 00 60"))
            # row 3
            .add(Paragraph("Mobile"))
            .add(Paragraph("+32 53 79 00 60"))
            # row 4
            .add(Paragraph("SSN"))
            .add(Paragraph("078-05-1120"))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_add_redact_annotation_001(self):

        # attempt to read PDF
        doc = None
        ls = [
            RegularExpressionTextExtraction(CommonRegularExpression.EMAIL.value),
        ]
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, ls)

        for l in ls:
            # fmt: off
            for m in l.get_matches_for_page(0):
                for bb in m.get_bounding_boxes():
                    doc.get_page(0).append_redact_annotation(bb, stroke_color=X11Color("Black"), fill_color=X11Color("Black"))
            # fmt: on

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
