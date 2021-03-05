import unittest

from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.toolkit.export.svg_export import SVGExport


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
        d0.add_event_listener(SVGExport())

        # check other listener(s)
        assert len(p0.get_event_listeners()) == 0
        assert len(d1.get_event_listeners()) == 0
        assert len(p1.get_event_listeners()) == 0
