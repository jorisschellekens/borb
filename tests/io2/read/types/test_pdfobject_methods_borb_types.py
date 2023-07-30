import unittest

import requests
from PIL import Image as PILImage  # type: ignore [import]

from borb.io.read.pdf_object import PDFObject
from borb.pdf.canvas.canvas import Canvas
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class TestPDFObjectMethodsBorbTypes(unittest.TestCase):
    """
    This test checks whether borb objects have the get_root method
    """

    def test_canvas_has_pdfobject_methods(self):

        # empty document
        obj0 = Canvas()

        # assert
        assert hasattr(obj0, "get_parent")
        assert hasattr(obj0, "get_reference")
        assert hasattr(obj0, "get_root")
        assert hasattr(obj0, "is_inline")
        assert hasattr(obj0, "is_unique")
        assert hasattr(obj0, "set_is_inline")
        assert hasattr(obj0, "set_is_unique")
        assert hasattr(obj0, "set_parent")
        assert hasattr(obj0, "set_reference")
        assert hasattr(obj0, "to_json")

    def test_document_has_pdfobject_methods(self):

        # empty document
        obj0 = Document()

        # assert
        assert hasattr(obj0, "get_parent")
        assert hasattr(obj0, "get_reference")
        assert hasattr(obj0, "get_root")
        assert hasattr(obj0, "is_inline")
        assert hasattr(obj0, "is_unique")
        assert hasattr(obj0, "set_is_inline")
        assert hasattr(obj0, "set_is_unique")
        assert hasattr(obj0, "set_parent")
        assert hasattr(obj0, "set_reference")
        assert hasattr(obj0, "to_json")

    def test_page_has_pdfobject_methods(self):

        # empty document
        obj0 = Page()

        # assert
        assert hasattr(obj0, "get_parent")
        assert hasattr(obj0, "get_reference")
        assert hasattr(obj0, "get_root")
        assert hasattr(obj0, "is_inline")
        assert hasattr(obj0, "is_unique")
        assert hasattr(obj0, "set_is_inline")
        assert hasattr(obj0, "set_is_unique")
        assert hasattr(obj0, "set_parent")
        assert hasattr(obj0, "set_reference")
        assert hasattr(obj0, "to_json")

    def test_image_has_pdfobject_methods(self):
        obj0 = PILImage.open(
            requests.get(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                stream=True,
            ).raw
        )
        PDFObject.add_pdf_object_methods(obj0)

        # assert
        assert hasattr(obj0, "get_parent")
        assert hasattr(obj0, "get_reference")
        assert hasattr(obj0, "get_root")
        assert hasattr(obj0, "is_inline")
        assert hasattr(obj0, "is_unique")
        assert hasattr(obj0, "set_is_inline")
        assert hasattr(obj0, "set_is_unique")
        assert hasattr(obj0, "set_parent")
        assert hasattr(obj0, "set_reference")
        # assert hasattr(obj0, "to_json")
