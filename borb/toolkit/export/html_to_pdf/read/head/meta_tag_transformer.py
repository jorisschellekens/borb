#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <meta> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.io.read.types import Dictionary, Name, String
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.xref.plaintext_xref import PlainTextXREF
from borb.toolkit.export.html_to_pdf.read.transformer import (
    Transformer,
)


class MetaTagTransformer(Transformer):
    """
    This implementation of BaseTagTransformer handles <meta> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <meta> element,
        False otherwise
        """
        return html_element.tag == "meta"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <meta> tag to its corresponding LayoutElement
        """
        if "name" not in html_element.attrib:
            return

        assert (
            len(html_element.getchildren()) == 0
        ), "<meta> children are currently not supported"
        assert (
            html_element.get("content") is not None
        ), "<meta> should have `content` attribute"

        name: str = html_element.get("name", "")
        content: str = html_element.get("content", "")

        document: typing.Optional[Document] = None
        if isinstance(layout_element, PageLayout):
            document = layout_element.get_page().get_root()  # type: ignore[attr-defined]
        if isinstance(layout_element, LayoutElement):
            document = layout_element.get_root()  # type: ignore[attr-defined]
        assert isinstance(document, Document)
        assert document is not None

        if "XRef" not in document:
            document[Name("XRef")] = PlainTextXREF()
        if "Trailer" not in document["XRef"]:
            document["XRef"][Name("Trailer")] = Dictionary()
            document["XRef"]["Trailer"].set_parent(document["XRef"])
        if "Info" not in document["XRef"]["Trailer"]:
            document["XRef"]["Trailer"][Name("Info")] = Dictionary()
            document["XRef"]["Trailer"]["Info"].set_parent(document["XRef"]["Trailer"])

        # description, keywords, author
        # set property
        name_remap: typing.Dict[str, str] = {
            "description": "Subject",
            "keywords": "Keywords",
            "author": "Author",
        }
        if name not in name_remap:
            return

        info_dictionary: Dictionary = document["XRef"]["Trailer"]["Info"]
        info_dictionary[Name(name_remap[name])] = String(content)
