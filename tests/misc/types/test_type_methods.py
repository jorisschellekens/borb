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

        # check methods
        assert hasattr(d0, "get_root")
        assert hasattr(p0, "get_root")
