import random
import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.ordered_list import OrderedList
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from borb.pdf.page_layout.two_column_layout import TwoColumnLayout
from borb.pdf.visitor.pdf import PDF


class TestTwoColumnLayout(unittest.TestCase):

    def test_two_column_layout_of_paragraphs(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: TwoColumnLayout = TwoColumnLayout(p)

        random.seed(0)
        for _ in range(0, 3):
            l.append_layout_element(
                Paragraph(
                    text=Lipsum.generate_lorem_ipsum(50),
                    font=Standard14Fonts.get("Helvetica-Bold"),
                    font_color=X11Color.YELLOW_MUNSELL,
                    font_size=20,
                )
            )
            for _ in range(0, 5):
                l.append_layout_element(
                    Paragraph(
                        text=Lipsum.generate_lorem_ipsum(500),
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                    )
                )

        PDF.write(what=d, where_to="assets/test_two_column_layout_of_paragraphs.pdf")

    def test_two_column_layout_of_images(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: TwoColumnLayout = TwoColumnLayout(p)

        random.seed(0)
        for _ in range(0, 3):
            l.append_layout_element(
                Paragraph(
                    text=Lipsum.generate_lorem_ipsum(50),
                    font=Standard14Fonts.get("Helvetica-Bold"),
                    font_color=X11Color.YELLOW_MUNSELL,
                    font_size=20,
                )
            )
            for _ in range(0, 5):
                l.append_layout_element(
                    Image(
                        "https://images.unsplash.com/photo-1492831379069-0fe9d118b7c5",
                        size=(100, 100),
                    )
                )

        PDF.write(what=d, where_to="assets/test_two_column_layout_of_images.pdf")

    def test_two_column_layout_of_tables(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: TwoColumnLayout = TwoColumnLayout(p)

        random.seed(0)
        for _ in range(0, 3):
            l.append_layout_element(
                Paragraph(
                    text=Lipsum.generate_lorem_ipsum(50),
                    font=Standard14Fonts.get("Helvetica-Bold"),
                    font_color=X11Color.YELLOW_MUNSELL,
                    font_size=20,
                )
            )
            for _ in range(0, 5):
                l.append_layout_element(
                    FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
                    .append_layout_element(Chunk("Lorem"))
                    .append_layout_element(Chunk("Ipsum"))
                    .append_layout_element(Chunk("Dolor"))
                    .append_layout_element(Chunk("Sit"))
                    .append_layout_element(Chunk("Amet"))
                    .append_layout_element(Chunk("Consectetur"))
                )

        PDF.write(what=d, where_to="assets/test_two_column_layout_of_tables.pdf")

    def test_two_column_layout_of_lists(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: TwoColumnLayout = TwoColumnLayout(p)

        random.seed(0)
        for _ in range(0, 3):
            l.append_layout_element(
                Paragraph(
                    text=Lipsum.generate_lorem_ipsum(50),
                    font=Standard14Fonts.get("Helvetica-Bold"),
                    font_color=X11Color.YELLOW_MUNSELL,
                    font_size=20,
                )
            )
            for _ in range(0, 5):
                l.append_layout_element(
                    OrderedList()
                    .append_layout_element(Chunk(text="Lorem"))
                    .append_layout_element(Chunk(text="Ipsum"))
                    .append_layout_element(Chunk(text="Dolor"))
                )

        PDF.write(what=d, where_to="assets/test_two_column_layout_of_lists.pdf")

    def test_two_column_layout_of_shapes(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: TwoColumnLayout = TwoColumnLayout(p)

        random.seed(0)
        for _ in range(0, 3):
            l.append_layout_element(
                Paragraph(
                    text=Lipsum.generate_lorem_ipsum(50),
                    font=Standard14Fonts.get("Helvetica-Bold"),
                    font_color=X11Color.YELLOW_MUNSELL,
                    font_size=20,
                )
            )
            for _ in range(0, 5):
                l.append_layout_element(
                    LineArt.blob(
                        stroke_color=X11Color.YELLOW_MUNSELL.darker(),
                        fill_color=X11Color.YELLOW_MUNSELL,
                    )
                )

        PDF.write(what=d, where_to="assets/test_two_column_layout_of_shapes.pdf")
