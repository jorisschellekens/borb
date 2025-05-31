import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestLineArtFractionOfCircleSmooth(unittest.TestCase):

    def test_line_art_fraction_of_circle_060_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=60).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_060_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_090_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=90).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_090_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_120_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=120).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_120_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_150_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=150).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_150_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_180_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=180).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_180_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_210_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=210).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_210_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_240_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=240).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_240_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_270_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=270).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_270_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_300_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=300).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_300_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_330_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=330).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_330_smooth.pdf"
        )

    def test_line_art_fraction_of_circle_360_smooth(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        LineArt.fraction_of_circle(angle_in_degrees=360).smooth().paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_line_art_fraction_of_circle_360_smooth.pdf"
        )
