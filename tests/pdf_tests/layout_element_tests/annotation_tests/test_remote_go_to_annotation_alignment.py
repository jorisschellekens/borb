import random
import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.remote_go_to_annotation import (
    RemoteGoToAnnotation,
)
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.visitor.pdf import PDF


class TestRemoteGoToAnnotationAlignment(unittest.TestCase):

    def test_remote_go_to_annotation_left_top(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_remote_go_to_annotation_left_top.pdf")

    def test_remote_go_to_annotation_left_middle(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_remote_go_to_annotation_left_middle.pdf"
        )

    def test_remote_go_to_annotation_left_bottom(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_remote_go_to_annotation_left_bottom.pdf"
        )

    def test_remote_go_to_annotation_middle_top(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_remote_go_to_annotation_middle_top.pdf")

    def test_remote_go_to_annotation_middle_middle(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_remote_go_to_annotation_middle_middle.pdf"
        )

    def test_remote_go_to_annotation_middle_bottom(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_remote_go_to_annotation_middle_bottom.pdf"
        )

    def test_remote_go_to_annotation_right_top(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_remote_go_to_annotation_right_top.pdf")

    def test_remote_go_to_annotation_right_middle(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_remote_go_to_annotation_right_middle.pdf"
        )

    def test_remote_go_to_annotation_right_bottom(self):
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

        # add RemoteGoToAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_remote_go_to_annotation_right_bottom.pdf"
        )
