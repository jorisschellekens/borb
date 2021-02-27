import logging
import random
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout, SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Justification,
    Paragraph,
)
from ptext.pdf.canvas.layout.shape import Shape
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../logs/test-write-100-stars.log", level=logging.DEBUG
)

import requests
from PIL import Image as PILImage


class TestWrite100Stars(unittest.TestCase):

    # fmt: off
    FIRST_100_STARS = [
        20948,      5761024,    6199849,    8897084,
        47014666,   30162978,   10934533,   14305330,
        28833521,   5593615,    6127739,    13665922,
        60891163,   40811120,   10265290,   25692082,
        38732059,   5165674,    9326700,    48793,
        47523691,   10300119,   1183729,    490222,
        38828319,   24482368,   445009,     10413016,
        28388427,   47697490,   26275724,   37651007,
        8905490,    355741,     5402068,    475578,
        35009,      12762442,   14140949,   65553994,
        12473742,   3680439,    43379688,   46769667,
        20150305,   32988819,   5372986,    66494041,
        2539015,    26300897,   2404461,    63579762,
        13872653,   60277705,   40031739,   175326,
        16610457,   214730,     33699775,   7403557,
        6440095,    19918901,   486331,     10211078,
        514888,     30214233,   5984934,    7837996,
        8367836,    10608766,   1114782,    8345813,
        1777629,    1889128,    20630069,   1728439,
        61306130,   2513172,    8989002,    11238,
        5347861,    1243475,    45919695,   236498,
        6311257,    6007526,    12981947,   887095,
        735802,     21070545,   6441339,    133845,
        4735784,    10510126,   769982,     20380,
        69243978,   12139796,   612826,     8690255,
    ]
    # fmt: on

    ACCENT_COLOR_1 = HexColor("F79F79")
    ACCENT_COLOR_2 = HexColor("F7D08A")
    ACCENT_COLOR_3 = HexColor("E3F09B")
    ACCENT_COLOR_4 = HexColor("87B6A7")
    ACCENT_COLOR_5 = HexColor("5B5941")

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../output/test-write-100-stars")

    def _write_background(self, page: Page):
        layout = SingleColumnLayout(page)
        t = Table(number_of_columns=10, number_of_rows=25)
        for i in range(0, 25):
            for j in range(0, 10):
                put_star = random.choice([x <= 3 for x in range(0, 10)])
                if i < 11 and j >= 5:
                    t.add(Paragraph(" "))
                    continue
                if put_star:
                    c = random.choice(
                        [
                            self.ACCENT_COLOR_1,
                            self.ACCENT_COLOR_2,
                            self.ACCENT_COLOR_3,
                            self.ACCENT_COLOR_4,
                            self.ACCENT_COLOR_5,
                        ]
                    )
                    t.add(
                        Shape(
                            LineArtFactory.n_pointed_star(
                                bounding_box=Rectangle(
                                    Decimal(0), Decimal(0), Decimal(16), Decimal(16)
                                ),
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

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        layout = MultiColumnLayout(page)

        # background
        self._write_background(page)

        # table
        avatar_urls = [
            "https://avatars.githubusercontent.com/u/" + str(x)
            for x in self.FIRST_100_STARS
        ]
        t = Table(number_of_columns=4, number_of_rows=25)
        for s in avatar_urls[0 : (4 * 25)]:
            im = PILImage.open(requests.get(s, stream=True).raw)
            t.add(Image(im, width=Decimal(20), height=Decimal(20)))
        t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        t.no_borders()
        layout.add(t)

        layout.add(
            Paragraph(
                "100 stars!",
                font="Helvetica-Bold",
                font_size=Decimal(20),
                font_color=self.ACCENT_COLOR_1,
                justification=Justification.CENTERED,
            )
        )

        # next column
        layout.switch_to_next_column()

        # paragraph
        layout.add(
            Paragraph(
                "Thank you,",
                font="Helvetica-Bold",
                font_size=Decimal(20),
                font_color=self.ACCENT_COLOR_1,
            )
        )
        layout.add(
            Paragraph(
                "Your support and encouragement have always been the driving factors in the development of pText. "
                "I want you to know that I value your appreciation immensely!"
            )
        )
        layout.add(
            Paragraph(
                "-- Joris Schellekens",
                font="Helvetica-Oblique",
                font_size=Decimal(8),
                font_color=self.ACCENT_COLOR_2,
            )
        )

        layout.add(
            Barcode(
                data="https://github.com/jorisschellekens/ptext-release/stargazers",
                type=BarcodeType.QR,
                width=Decimal(128),
                stroke_color=self.ACCENT_COLOR_1,
            )
        )

        # footer
        rectangle_box = Rectangle(
            Decimal(0),
            Decimal(0),
            page.get_page_info().get_width(),
            page.get_page_info().get_height() * Decimal(0.1),
        )
        Shape(
            LineArtFactory.rectangle(rectangle_box),
            fill_color=self.ACCENT_COLOR_1,
            stroke_color=self.ACCENT_COLOR_1,
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
            fill_color=self.ACCENT_COLOR_2,
            stroke_color=self.ACCENT_COLOR_2,
            line_width=Decimal(1),
        ).layout(page, rectangle_box)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
