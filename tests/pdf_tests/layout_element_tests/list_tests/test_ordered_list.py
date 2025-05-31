import random
import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.list.ordered_list import OrderedList
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestOrderedList(unittest.TestCase):

    def test_ordered_list_of_annotations(self):
        pass

    def test_ordered_list_of_forms(self):
        pass

    def test_ordered_list_of_images(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            OrderedList()
            .append_layout_element(
                Image(
                    bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1492831379069-0fe9d118b7c5",
                    size=(100, 100),
                    padding_bottom=10,
                )
            )
            .append_layout_element(
                Image(
                    bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1501438400798-b40ff50396c8",
                    size=(100, 100),
                    padding_bottom=10,
                )
            )
            .append_layout_element(
                Image(
                    bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1458791087439-278afc90b1d5",
                    size=(100, 100),
                    padding_bottom=10,
                )
            )
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to="assets/test_ordered_list_of_images.pdf")

    def test_ordered_list_of_lists(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            OrderedList()
            .append_layout_element(
                OrderedList()
                .append_layout_element(Chunk("Lorem"))
                .append_layout_element(Chunk("Ipsum"))
                .append_layout_element(Chunk("Dolor"))
            )
            .append_layout_element(
                OrderedList()
                .append_layout_element(Chunk("Sit"))
                .append_layout_element(Chunk("Amet"))
                .append_layout_element(Chunk("Consectetur"))
            )
            .append_layout_element(
                OrderedList()
                .append_layout_element(Chunk("Adipiscing"))
                .append_layout_element(Chunk("Elit"))
                .append_layout_element(Chunk("Sed"))
            )
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to="assets/test_ordered_list_of_lists.pdf")

    def test_ordered_list_of_shapes(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        random.seed(0)
        (
            OrderedList()
            .append_layout_element(
                LineArt.blob(
                    stroke_color=X11Color.ALICE_BLUE.darker(),
                    fill_color=X11Color.ALICE_BLUE,
                ).scale_to_fit(size=(100, 100))
            )
            .append_layout_element(
                LineArt.blob(
                    stroke_color=X11Color.BEIGE.darker(), fill_color=X11Color.BEIGE
                ).scale_to_fit(size=(100, 100))
            )
            .append_layout_element(
                LineArt.blob(
                    stroke_color=X11Color.CADET_BLUE.darker(),
                    fill_color=X11Color.CADET_BLUE,
                ).scale_to_fit(size=(100, 100))
            )
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to="assets/test_ordered_list_of_shapes.pdf")

    def test_ordered_list_of_text(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            OrderedList()
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to="assets/test_ordered_list_of_text.pdf")
