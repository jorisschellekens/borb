from borb.pdf import (
    Document,
    Page,
    PageLayout,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    X11Color,
)
from tests.test_case import TestCase


class TestReadWrite(TestCase):

    def test_read_write(self):

        # STEP 1: create PDF
        d: Document = Document()
        p: Page = Page()
        d.append_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(32), font_color=X11Color.YELLOW_MUNSELL
            )
        )
        TestCase.write(what=d, where_to="test_read_write.pdf")

        # STEP 2: read PDF
        d = TestCase.read(where_from="test_read_write.pdf")

        # STEP 3: add content to PDF
        p = d.get_page(0)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Paragraph(
            Lipsum.generate_lorem_ipsum(32), font_color=X11Color.PRUSSIAN_BLUE
        ).paint(available_space=(x, y, w, h - 15), page=p)

        # STEP 4: write PDF
        TestCase.write(what=d, where_to="test_read_write_b.pdf")
