import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


@unittest.skip
class TestLineArtLissajours(unittest.TestCase):

    def test_line_art_lissajours_001_001(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=1, y_frequency=1).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_001_001.pdf", d)

    def test_line_art_lissajours_001_002(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=1, y_frequency=2).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_001_002.pdf", d)

    def test_line_art_lissajours_001_003(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=1, y_frequency=3).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_001_003.pdf", d)

    def test_line_art_lissajours_002_001(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=2, y_frequency=1).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_002_001.pdf", d)

    def test_line_art_lissajours_002_002(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=2, y_frequency=2).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_002_002.pdf", d)

    def test_line_art_lissajours_002_003(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=2, y_frequency=3).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_002_003.pdf", d)

    def test_line_art_lissajours_003_001(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=3, y_frequency=1).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_003_001.pdf", d)

    def test_line_art_lissajours_003_002(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=3, y_frequency=2).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_003_002.pdf", d)

    def test_line_art_lissajours_003_003(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.lissajours(x_frequency=3, y_frequency=3).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write("assets/test_line_art_lissajours_003_003.pdf", d)
