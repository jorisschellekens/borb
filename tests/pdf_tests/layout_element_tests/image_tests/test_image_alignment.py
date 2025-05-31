import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestImageAlignment(unittest.TestCase):

    def test_image_alignment_left_top(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_left_top.pdf")

    def test_image_alignment_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_left_middle.pdf")

    def test_image_alignment_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_left_bottom.pdf")

    def test_image_alignment_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_middle_top.pdf")

    def test_image_alignment_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_middle_middle.pdf")

    def test_image_alignment_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_middle_bottom.pdf")

    def test_image_alignment_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_right_top.pdf")

    def test_image_alignment_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_right_middle.pdf")

    def test_image_alignment_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to=f"assets/test_image_alignment_right_bottom.pdf")
