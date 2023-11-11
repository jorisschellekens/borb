from decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import ChunkOfText
from borb.pdf import ConnectedShape
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import LineArtFactory
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.geometry.rectangle import Rectangle
from tests.test_case import TestCase


class TestZapfDingbatsMetrics(TestCase):
    def test_zapfdingbats_metrics_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a ChunkOfText to the PDF with a Zapfdingbats character, in font_size 24"
            )
        )
        e = ChunkOfText(
            "●",
            font="Zapfdingbats",
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            border_color=HexColor("#ff0000"),
            font_size=Decimal(24),
        )
        layout.add(e)
        print(e.get_previous_layout_box().get_x())
        print(e.get_previous_layout_box().get_y())
        print(e.get_previous_layout_box().get_width())
        print(e.get_previous_layout_box().get_height())

        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_zapfdingbats_metrics_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a ChunkOfText to the PDF with a Zapfdingbats character, in font_size 24, aligned TOP"
            )
        )

        e = ChunkOfText(
            "●",
            font="Zapfdingbats",
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            border_color=HexColor("#00ff00"),
            font_size=Decimal(24),
            vertical_alignment=Alignment.TOP,
        )

        layout_rect: Rectangle = Rectangle(
            Decimal(59.5),
            Decimal(608.2) - Decimal(20),
            Decimal(20.24),
            Decimal(30.79) + Decimal(20),
        )
        ConnectedShape(
            LineArtFactory.rectangle(layout_rect),
            line_width=Decimal(0.1),
            stroke_color=HexColor("#ff0000"),
            fill_color=None,
        ).paint(page, layout_rect)

        e.paint(page, layout_rect)

        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_zapfdingbats_metrics_003(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a ChunkOfText to the PDF with a Zapfdingbats character, in font_size 24, aligned MIDDLE"
            )
        )

        e = ChunkOfText(
            "●",
            font="Zapfdingbats",
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            border_color=HexColor("#00ff00"),
            font_size=Decimal(24),
            vertical_alignment=Alignment.MIDDLE,
        )

        layout_rect: Rectangle = Rectangle(
            Decimal(59.5),
            Decimal(608.2) - Decimal(20),
            Decimal(20.24),
            Decimal(30.79) + Decimal(20),
        )
        ConnectedShape(
            LineArtFactory.rectangle(layout_rect),
            line_width=Decimal(0.1),
            stroke_color=HexColor("#ff0000"),
            fill_color=None,
        ).paint(page, layout_rect)

        e.paint(page, layout_rect)

        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_zapfdingbats_metrics_004(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a ChunkOfText to the PDF with a Zapfdingbats character, in font_size 24, aligned BOTTOM"
            )
        )

        e = ChunkOfText(
            "●",
            font="Zapfdingbats",
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            border_color=HexColor("#00ff00"),
            font_size=Decimal(24),
            vertical_alignment=Alignment.BOTTOM,
        )

        layout_rect: Rectangle = Rectangle(
            Decimal(59.5),
            Decimal(608.2) - Decimal(20),
            Decimal(20.24),
            Decimal(30.79) + Decimal(20),
        )
        ConnectedShape(
            LineArtFactory.rectangle(layout_rect),
            line_width=Decimal(0.1),
            stroke_color=HexColor("#ff0000"),
            fill_color=None,
        ).paint(page, layout_rect)

        e.paint(page, layout_rect)

        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())
