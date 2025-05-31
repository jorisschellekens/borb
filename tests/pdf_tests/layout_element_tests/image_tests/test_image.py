import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.image import Image
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestImage(unittest.TestCase):

    def test_image(self):
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
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_image.pdf")
