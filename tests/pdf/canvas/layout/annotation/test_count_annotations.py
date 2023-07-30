import typing
import unittest
from decimal import Decimal

from borb.io.read.types import List
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.circle_annotation import CircleAnnotation
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestCountAnnotations(TestCase):
    def test_add_circle_annotations(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an empty Page, and nine circle annotations"
            )
        )

        # add annotation
        w: Decimal = pdf.get_page(0).get_page_info().get_width()
        h: Decimal = pdf.get_page(0).get_page_info().get_height()
        for i in range(0, 3):
            for j in range(0, 3):
                pdf.get_page(0).add_annotation(
                    CircleAnnotation(
                        bounding_box=Rectangle(
                            w / Decimal(2) - Decimal(32 * 1.5) + i * 32,
                            h / Decimal(2) - Decimal(32 * 1.5) + j * 32,
                            Decimal(32),
                            Decimal(32),
                        ),
                        stroke_color=HexColor("0B3954"),
                        fill_color=HexColor("f1cd2e"),
                    )
                )

        # attempt to store PDF
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_count_annotations(self):
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)
        assert doc is not None
        page: Page = doc.get_page(0)
        assert page is not None
        assert "Annots" in page
        assert isinstance(page["Annots"], List)
        assert len(page["Annots"]) == 9
