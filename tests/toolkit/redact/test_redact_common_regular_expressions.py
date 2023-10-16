import typing
import unittest
from decimal import Decimal

from borb.io.read.types import List
from borb.pdf import HexColor
from borb.pdf.canvas.layout.annotation.redact_annotation import RedactAnnotation
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.redact.common_regular_expressions import CommonRegularExpression
from borb.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestRedactCommonRegularExpressions(TestCase):
    def test_create_dummy_pdf(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a table of (commonly deemed) sensitive information, "
                "such as social security number, email, etc. "
                "A subsequent test will then look for those patterns and redact them."
            )
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
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_add_redact_annotation_for_email(self):

        # attempt to read PDF
        doc = None
        ls = [
            RegularExpressionTextExtraction(CommonRegularExpression.EMAIL.value),
        ]
        with open(self.get_first_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, ls)

        for l in ls:
            # fmt: off
            for m in l.get_matches()[0]:
                for bb in m.get_bounding_boxes():
                    doc.get_page(0).add_annotation(RedactAnnotation(bb,
                                                                    stroke_color=HexColor("000000"),
                                                                    fill_color=HexColor("000000")
                                                                    )
                                                   )
            # fmt: on

        # attempt to store PDF
        with open(self.get_second_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_apply_redact_annotation_for_email(self):

        doc: typing.Optional[Document] = None
        with open(self.get_second_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)
        assert doc is not None

        page: Page = doc.get_page(0)
        assert page is not None
        assert "Annots" in page
        assert isinstance(page["Annots"], List)
        assert len(page["Annots"]) == 1

        # apply redaction annotations
        doc.get_page(0).apply_redact_annotations()

        # attempt to store PDF
        with open(self.get_third_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
