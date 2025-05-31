import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.unsplash import Unsplash
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestUnsplash(unittest.TestCase):

    def test_unsplash(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        try:
            from tests.secrets import populate_os_environ

            populate_os_environ()
        except:
            pass

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Unsplash(
            keywords=["cherry", "blossom"],
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_unsplash.pdf")
