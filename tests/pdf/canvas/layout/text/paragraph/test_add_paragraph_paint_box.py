import random
import typing
from decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import ConnectedShape
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import LineArtFactory
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.geometry.rectangle import Rectangle
from tests.test_case import TestCase


class TestAddParagraphPaintBox(TestCase):
    def test_add_paragraph_paint_box(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a Paragraph to the PDF."
            )
        )

        # determine text
        random.seed(0)
        text: str = Lipsum.generate_lipsum_text(1)

        # set bounding box
        bounding_box: Rectangle = Rectangle(
            Decimal(100), Decimal(100), Decimal(100), Decimal(100)
        )

        # render
        font_size_that_fits: typing.Optional[Decimal] = None
        for fs in [12, 11, 10, 9, 8, 7, 6, 5]:
            try:
                Paragraph(
                    text, text_alignment=Alignment.JUSTIFIED, font_size=Decimal(fs)
                ).paint(page=page, available_space=bounding_box)
                font_size_that_fits = Decimal(fs)
                break
            except:
                pass

        assert font_size_that_fits == 10

        # draw line
        ConnectedShape(
            LineArtFactory.rectangle(bounding_box),
            stroke_color=HexColor("#ff0000"),
            fill_color=None,
        ).paint(page=page, available_space=bounding_box)

        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
