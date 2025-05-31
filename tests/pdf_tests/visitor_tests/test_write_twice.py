import copy
import unittest

from borb.pdf import (
    Document,
    PageLayout,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    Page,
    PDF,
)


class TestWriteTwice(unittest.TestCase):

    def test_write_twice_with_copy(self):

        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))

        d2 = copy.deepcopy(d1)
        PDF.write(what=d1, where_to="assets/test_write_twice_with_copy_001.pdf")
        PDF.write(what=d2, where_to="assets/test_write_twice_with_copy_002.pdf")

    def test_write_twice_without_copy(self):

        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))

        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_001.pdf")
        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_002.pdf")
