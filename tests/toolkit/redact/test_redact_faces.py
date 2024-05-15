import unittest
from decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import Image
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.toolkit import FaceDetectionEventListener
from borb.toolkit import FaceEraserEventListener
from tests.test_case import TestCase


class TestRedactFaces(TestCase):
    def test_create_dummy_pdf(self):
        d: Document = Document()

        p: Page = Page()
        d.add_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.add(Paragraph(Lipsum.generate_lipsum_text(5)))
        l.add(
            FlexibleColumnWidthTable(
                number_of_columns=2,
                number_of_rows=2,
                horizontal_alignment=Alignment.CENTERED,
            )
            .add(
                Image(
                    "https://images.unsplash.com/photo-1438761681033-6461ffad8d80",
                    width=Decimal(128),
                    height=Decimal(128),
                )
            )
            .add(
                Image(
                    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d",
                    width=Decimal(128),
                    height=Decimal(128),
                )
            )
            .add(
                Image(
                    "https://images.unsplash.com/photo-1548142813-c348350df52b",
                    width=Decimal(128),
                    height=Decimal(128),
                )
            )
            .add(
                Image(
                    "https://images.unsplash.com/photo-1624224971170-2f84fed5eb5e",
                    width=Decimal(128),
                    height=Decimal(128),
                )
            )
            .set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
            .no_borders()
        )

        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, d)

    @unittest.skip
    def test_redact_faces(self):
        # create PDF
        self.test_create_dummy_pdf()

        # read (and extract faces)
        l: FaceDetectionEventListener = FaceEraserEventListener()
        with open(self.get_first_output_file(), "rb") as fh:
            d = PDF.loads(fh, [l])

        # store
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, d)
