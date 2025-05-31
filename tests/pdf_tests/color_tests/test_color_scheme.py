import math
import typing
import unittest

from borb.pdf.color.color import Color
from borb.pdf.color.color_scheme import ColorScheme
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestColorScheme(unittest.TestCase):

    def test_color_scheme_complimentary_colors(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [X11Color.YELLOW_MUNSELL] + [
            ColorScheme.complementary_color(X11Color.YELLOW_MUNSELL)
        ]

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_color_scheme_complimentary_colors.pdf")

    def test_color_scheme_analogous_colors(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [
            X11Color.YELLOW_MUNSELL
        ] + ColorScheme.analogous_colors(X11Color.YELLOW_MUNSELL)

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_color_scheme_analogous_colors.pdf")

    def test_color_scheme_triadic_colors(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [
            X11Color.YELLOW_MUNSELL
        ] + ColorScheme.triadic_colors(X11Color.YELLOW_MUNSELL)

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_color_scheme_triadic_colors.pdf")

    def test_color_scheme_tetradic_colors(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [
            X11Color.YELLOW_MUNSELL
        ] + ColorScheme.tetradic_colors(X11Color.YELLOW_MUNSELL)

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_color_scheme_tetradic_colors.pdf")

    def test_color_scheme_split_complementary_colors(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [
            X11Color.YELLOW_MUNSELL
        ] + ColorScheme.split_complementary_colors(X11Color.YELLOW_MUNSELL)

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(
            what=d, where_to="assets/test_color_scheme_split_complementary_colors.pdf"
        )

    def test_color_scheme_shades(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = ColorScheme.shades(
            X11Color.YELLOW_MUNSELL, steps=10
        )

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_color_scheme_shades.pdf")

    def test_color_scheme_tints(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [X11Color.YELLOW_MUNSELL] + ColorScheme.tints(
            X11Color.YELLOW_MUNSELL, steps=10
        )

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_color_scheme_tints.pdf")

    def test_color_scheme_monochromatic(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # create Color object(s)
        colors: typing.List[Color] = [
            X11Color.YELLOW_MUNSELL
        ] + ColorScheme.monochromatic(X11Color.YELLOW_MUNSELL, steps=10)

        N: int = int(math.sqrt(len(colors))) + 1
        k: int = 0
        for i in range(0, N):
            for j in range(0, N):
                if k >= len(colors):
                    continue
                x: int = p.get_size()[0] // 2 - (N * 20) // 2 + i * 20
                y: int = p.get_size()[1] // 2 - (N * 20) // 2 + j * 20
                LineArt.square(
                    stroke_color=X11Color.WHITE, fill_color=colors[k]
                ).scale_by_factor(x_factor=20 / 100, y_factor=20 / 100).paint(
                    available_space=(x, y, 20, 20), page=p
                )
                k += 1

        PDF.write(what=d, where_to="assets/test_color_scheme_monochromatic.pdf")
