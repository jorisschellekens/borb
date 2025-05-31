import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.text.code_snippet import CodeSnippet
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestCodeSnippetBackground(unittest.TestCase):

    def test_code_snippet_background(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        CodeSnippet(
            code="""
            def fib(n: int) -> int:
                if n == 0 or n == 1:
                    return 1
                else:
                    return fib(n-1) + fib(n-2)
            """,
            padding_top=10,
            padding_right=10,
            padding_bottom=10,
            padding_left=10,
            background_color=X11Color.YELLOW_MUNSELL,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_code_snippet_background.pdf")
