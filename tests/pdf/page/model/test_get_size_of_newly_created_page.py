import unittest

from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class TestGetSizeOfNewlyCreatedPage(unittest.TestCase):
    def test_get_size_of_newly_created_page(self):
        p: Page = Page()
        assert p.get_page_info().get_width() == 595
        assert p.get_page_info().get_height() == 842

    def test_get_size_of_newly_created_page_by_document(self):
        d: Document = Document()
        d.append_page(Page())
        assert d.get_page(0).get_page_info().get_width() == 595
        assert d.get_page(0).get_page_info().get_height() == 842
