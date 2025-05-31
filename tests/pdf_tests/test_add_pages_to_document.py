import unittest

from borb.pdf import (
    Document,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    X11Color,
    Page,
    PDF,
)


class TestAddPagesToDocument(unittest.TestCase):

    def test_add_pages_to_document(self):

        # first document
        doc01: Document = Document()
        page: Page = Page()
        doc01.append_page(page)
        layout: SingleColumnLayout = SingleColumnLayout(page)
        for _ in range(0, 5):
            layout.append_layout_element(
                Paragraph(
                    Lipsum.generate_lorem_ipsum(512), font_color=X11Color.YELLOW_MUNSELL
                )
            )
        # PDF.write(what=doc01, where_to='assets/test_add_pages_to_document_01.pdf')

        # second document
        doc02: Document = Document()
        page: Page = Page()
        doc02.append_page(page)
        layout: SingleColumnLayout = SingleColumnLayout(page)
        for _ in range(0, 5):
            layout.append_layout_element(
                Paragraph(
                    Lipsum.generate_lorem_ipsum(512), font_color=X11Color.PRUSSIAN_BLUE
                )
            )
        # PDF.write(what=doc02, where_to='assets/test_add_pages_to_document_02.pdf')

        # merge
        doc01.append_page(doc02.get_page(0))
        PDF.write(what=doc01, where_to="assets/test_add_pages_to_document_03.pdf")
