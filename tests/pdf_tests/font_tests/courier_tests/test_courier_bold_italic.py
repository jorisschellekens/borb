import unittest

from borb.pdf.document import Document
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestCourierBoldItalic(unittest.TestCase):

    def test_courier_bold_italic(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        font: Font = Standard14Fonts.get("Courier Bold Italic")
        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
        line_height: int = int(12 * 1.2)

        # paint Chunk(s)
        Chunk(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do", font=font
        ).paint(available_space=(x, y, w, h), page=p)
        Chunk(
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim",
            font=font,
        ).paint(available_space=(x, y, w, h - line_height), page=p)
        Chunk(
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
            font=font,
        ).paint(available_space=(x, y, w, h - 2 * line_height), page=p)
        Chunk(
            "aliquip ex ea commodo consequat. Duis aute irure dolor in", font=font
        ).paint(available_space=(x, y, w, h - 3 * line_height), page=p)
        Chunk(
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
            font=font,
        ).paint(available_space=(x, y, w, h - 4 * line_height), page=p)
        Chunk("pariatur.", font=font).paint(
            available_space=(x, y, w, h - 5 * line_height), page=p
        )

        PDF.write(what=d, where_to="assets/test_courier_bold_italic.pdf")
