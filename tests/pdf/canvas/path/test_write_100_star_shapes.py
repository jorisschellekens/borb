import logging
import random
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color, Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Paragraph,
)
from ptext.pdf.canvas.layout.shape import Shape
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../logs/test-write-100-star-shapes.log", level=logging.DEBUG
)


class TestWrite100StarShapes(unittest.TestCase):

    COLORS = [
        X11Color("Red"),
        X11Color("Orange"),
        X11Color("Yellow"),
        X11Color("YellowGreen"),
        X11Color("Blue"),
        X11Color("Purple"),
    ]

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../output/test-write-100-star-shapes")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        layout = SingleColumnLayout(page)
        t = Table(number_of_columns=10, number_of_rows=25)
        for _ in range(0, 10):
            for _ in range(0, 25):
                put_star = random.choice([x <= 3 for x in range(0, 10)])
                if put_star:
                    c: Color = random.choice(self.COLORS)
                    s: Decimal = random.choice(
                        [
                            Decimal(16),
                            Decimal(16),
                            Decimal(16),
                            Decimal(16),
                            Decimal(8),
                            Decimal(4),
                        ]
                    )
                    t.add(
                        Shape(
                            LineArtFactory.n_pointed_star(
                                bounding_box=Rectangle(Decimal(0), Decimal(0), s, s),
                                n=random.choice([3, 5, 7, 12]),
                            ),
                            fill_color=c,
                            stroke_color=c,
                            line_width=Decimal(1),
                        )
                    )
                else:
                    t.add(Paragraph(" "))
        t.no_borders()
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        layout.add(t)

        # footer
        rectangle_box = Rectangle(
            Decimal(0),
            Decimal(0),
            page.get_page_info().get_width(),
            page.get_page_info().get_height() * Decimal(0.1),
        )
        Shape(
            LineArtFactory.rectangle(rectangle_box),
            fill_color=self.COLORS[0],
            stroke_color=self.COLORS[0],
            line_width=Decimal(1),
        ).layout(page, rectangle_box)

        rectangle_box = Rectangle(
            Decimal(0),
            page.get_page_info().get_height() * Decimal(0.1),
            page.get_page_info().get_width(),
            Decimal(2),
        )
        Shape(
            LineArtFactory.rectangle(rectangle_box),
            fill_color=self.COLORS[1],
            stroke_color=self.COLORS[1],
            line_width=Decimal(1),
        ).layout(page, rectangle_box)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
