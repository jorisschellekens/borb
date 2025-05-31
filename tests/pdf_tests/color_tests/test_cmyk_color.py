import math
import typing
import unittest

from borb.pdf.color.cmyk_color import CMYKColor
from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestCMYKColor(unittest.TestCase):

    def test_cmyk_color(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [
            CMYKColor(cyan=(i // 10) / 9, magenta=(i % 10) / 9, yellow=0.33, key=0.33)
            for i in range(0, 100)
        ]

        N: int = int(math.sqrt(len(colors)))
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_cmyk_color.pdf")
