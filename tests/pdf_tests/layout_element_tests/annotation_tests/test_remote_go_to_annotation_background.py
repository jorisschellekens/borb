import random
import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.remote_go_to_annotation import (
    RemoteGoToAnnotation,
)
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestRemoteGoToAnnotationBackground(unittest.TestCase):

    def test_remote_go_to_annotation_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # add some text to highlight
        random.seed(0)
        Paragraph(
            text=Lipsum.generate_lorem_ipsum(50),
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
        ).paint(available_space=(x, y, 100, h), page=p)

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
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

        PDF.write(what=d, where_to="assets/test_remote_go_to_annotation_background.pdf")
