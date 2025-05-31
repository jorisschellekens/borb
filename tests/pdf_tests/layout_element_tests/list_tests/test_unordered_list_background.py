import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestUnorderedListBackground(unittest.TestCase):

    def test_unordered_list_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            UnorderedList(
                background_color=X11Color.YELLOW_MUNSELL,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to=f"assets/test_unordered_list_background.pdf")
