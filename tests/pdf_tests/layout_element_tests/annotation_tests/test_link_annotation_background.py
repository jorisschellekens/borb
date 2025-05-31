import random
import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.link_annotation import LinkAnnotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.visitor.pdf import PDF


class TestLinkAnnotationBackground(unittest.TestCase):

    def test_link_annotation_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # generate random text
        random.seed(0)
        l: PageLayout = SingleColumnLayout(p)
        for _ in range(0, 10):
            l.append_layout_element(
                Paragraph(
                    Lipsum.generate_lorem_ipsum(512),
                    text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                )
            )

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # add LinkAnnotation
        LinkAnnotation(
            link_to_page_nr=1,
            size=(100, 100),
            background_color=X11Color.YELLOW_MUNSELL,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_link_annotation_background.pdf")
