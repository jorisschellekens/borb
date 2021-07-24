import unittest

from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.pdf_to_svg import PDFToSVG


class TestTypeMethods(unittest.TestCase):
    def test_type_methods(self):

        # first document
        d0 = Document()
        p0 = Page()
        d0.append_page(p0)

        # second document
        d1 = Document()
        p1 = Page()
        d1.append_page(p1)

        # add listener to d0
        d0.add_event_listener(PDFToSVG())

        # check other listener(s)
        assert len(p0.get_event_listeners()) == 0
        assert len(d1.get_event_listeners()) == 0
        assert len(p1.get_event_listeners()) == 0
