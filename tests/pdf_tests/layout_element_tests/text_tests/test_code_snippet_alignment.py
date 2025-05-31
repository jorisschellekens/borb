import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.code_snippet import CodeSnippet
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestCodeSnippetAlignment(unittest.TestCase):

    @staticmethod
    def get_code_snippet(
        h: LayoutElement.HorizontalAlignment, v: LayoutElement.VerticalAlignment
    ) -> CodeSnippet:
        return CodeSnippet(
            code="""
                def fib(n: int) -> int:
                    if n == 0 or n == 1:
                        return 1
                    else:
                        return fib(n-1) + fib(n-2)
                """,
            horizontal_alignment=h,
            vertical_alignment=v,
        )

    def test_code_snippet_alignment_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_left_top.pdf",
        )

    def test_code_snippet_alignment_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_left_middle.pdf",
        )

    def test_code_snippet_alignment_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_left_bottom.pdf",
        )

    def test_code_snippet_alignment_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_middle_top.pdf",
        )

    def test_code_snippet_alignment_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_middle_middle.pdf",
        )

    def test_code_snippet_alignment_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_middle_bottom.pdf",
        )

    def test_code_snippet_alignment_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_right_top.pdf",
        )

    def test_code_snippet_alignment_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_right_middle.pdf",
        )

    def test_code_snippet_alignment_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestCodeSnippetAlignment.get_code_snippet(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_code_snippet_alignment_right_bottom.pdf",
        )
