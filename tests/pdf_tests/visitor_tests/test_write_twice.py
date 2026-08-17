import copy
import random

from borb.pdf import (
    Document,
    PageLayout,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    Page,
    PDF,
    LineArt,
    Image,
    TextAnnotation,
    TableUtil,
)
from tests.test_case import TestCase


class TestWriteTwice(TestCase):

    def test_write_twice_with_copy(self):

        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        random.seed(0)
        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))

        d2 = copy.deepcopy(d1)
        TestCase.write(what=d1, where_to="assets/test_write_twice_with_copy_a.pdf")
        TestCase.write(what=d2, where_to="assets/test_write_twice_with_copy_b.pdf")

    def test_write_read_write_without_copy(self):

        # write
        d1: Document = Document()
        p: Page = Page()
        d1.append_page(p)
        l: PageLayout = SingleColumnLayout(p)

        # add text
        random.seed(0)
        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))

        # add rectangle
        l.append_layout_element(LineArt.rectangle())

        # add annotation
        l.append_layout_element(TextAnnotation(contents="Lorem ipsum"))

        # add image
        l.append_layout_element(
            Image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm0Wq_2sTfpM9NisExXWpwhvxr5bPO2IUPfg&s",
                size=(100, 100),
            )
        )

        # add table
        l.append_layout_element(
            TableUtil.from_2d_data(
                [["Lorem", "Ipsum"], [1, 2], [3, 4]]
            ).set_padding_on_all_cells(5, 5, 5, 5)
        )
        TestCase.write(what=d1, where_to="test_write_read_write_without_copy_a.pdf")

        # read
        d1 = TestCase.read(where_from="test_write_read_write_without_copy_a.pdf")

        # write
        TestCase.write(what=d1, where_to="test_write_read_write_without_copy_b.pdf")

    def test_write_twice_without_copy(self):

        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))

        TestCase.write(what=d1, where_to="assets/test_write_twice_without_copy_a.pdf")
        TestCase.write(what=d1, where_to="assets/test_write_twice_without_copy_b.pdf")

    def test_write_twice_without_copy_002(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(LineArt.rectangle())

        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_002_a.pdf"
        )
        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_002_b.pdf"
        )

    def test_write_twice_without_copy_003(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(
            Image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm0Wq_2sTfpM9NisExXWpwhvxr5bPO2IUPfg&s",
                size=(100, 100),
            )
        )

        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_003_a.pdf"
        )
        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_003_b.pdf"
        )

    def test_write_twice_without_copy_004(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(TextAnnotation(contents="Lorem ipsum"))

        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_004_a.pdf"
        )
        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_004_b.pdf"
        )

    def test_write_twice_without_copy_005(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(
            TableUtil.from_2d_data(
                [["Lorem", "Ipsum"], [1, 2], [3, 4]]
            ).set_padding_on_all_cells(5, 5, 5, 5)
        )

        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_005_a.pdf"
        )
        TestCase.write(
            what=d1, where_to="assets/test_write_twice_without_copy_005_b.pdf"
        )
