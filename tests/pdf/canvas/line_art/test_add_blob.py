import random

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.line_art.blob_factory import BlobFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddBlob(TestCase):
    """
    This test creates a PDF with a Blob in it
    """

    def test_add_blob_using_3_points(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test generates a PDF containing a ConnectedShape object using the BlobFactory."
            )
        )
        random.seed(2048)
        layout.add(
            ConnectedShape(
                points=BlobFactory.blob(3),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                line_width=Decimal(1),
            ).scale_up(Decimal(200), Decimal(200))
        )
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_blob_using_4_points(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test generates a PDF containing a ConnectedShape object using the BlobFactory."
            )
        )
        random.seed(2048)
        layout.add(
            ConnectedShape(
                points=BlobFactory.blob(4),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                line_width=Decimal(1),
            ).scale_up(Decimal(200), Decimal(200))
        )
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.check_pdf_using_validator(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_add_blob_using_5_points(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test generates a PDF containing a ConnectedShape object using the BlobFactory."
            )
        )
        random.seed(2048)
        layout.add(
            ConnectedShape(
                points=BlobFactory.blob(5),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                line_width=Decimal(1),
            ).scale_up(Decimal(200), Decimal(200))
        )
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.check_pdf_using_validator(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file())
