import time
import typing
import unittest

from borb.pdf.document import Document
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestHeterogeneousParagraph(unittest.TestCase):

    def build_temporary_document(self) -> float:
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        delta: float = time.time()
        HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                Chunk("Ut enim", font=Standard14Fonts.get("Helvetica-Bold")),
                Chunk(
                    "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )
        delta = time.time() - delta

        # persist
        PDF.write(what=d, where_to="assets/build_temporary_document.pdf")

        # return
        return delta

    def test_heterogeneous_paragraph_speed(self):

        layout_speed_in_seconds: typing.List[float] = []
        for i in range(0, 100):
            layout_speed_in_seconds += [self.build_temporary_document()]
            print(f"{i:03d}: {round(layout_speed_in_seconds[-1], 5)}s")

        # print average
        avg: float = sum(layout_speed_in_seconds) / len(layout_speed_in_seconds)
        print(f"AVG: {round(avg, 5)}s")

        assert 0 < avg < 0.005
