import unittest

from borb.pdf import RemoteGoToAnnotation, Document, Page


class TestRemoteGoToAnnotationHeight(unittest.TestCase):

    def test_remote_go_to_annotation_height_12(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # add HighlightAnnotation
        RemoteGoToAnnotation(
            uri="http://www.borbpdf.com/",
            size=(100, 100),
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_remote_go_to_annotation_height_12.pdf")