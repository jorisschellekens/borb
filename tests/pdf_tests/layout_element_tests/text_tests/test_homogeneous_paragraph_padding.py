import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.text.homogeneous_paragraph import HomogeneousParagraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestHeterogeneousParagraph(unittest.TestCase):

    def test_homogeneous_paragraph(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        HomogeneousParagraph(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            "Ut enim"
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 200 // 2,
                p.get_size()[1] // 2 - 200 // 2,
                200,
                200,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_homogeneous_paragraph.pdf")

        # TODO
