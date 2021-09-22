#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <body> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.html_to_pdf.read.transformer import (
    Transformer,
)


class BodyTagTransformer(Transformer):
    """
    This implementation of BaseTagTransformer handles <body> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <body> element,
        False otherwise
        """
        return html_element.tag == "body"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <body> tag to its corresponding LayoutElement
        """

        # leading text
        leading_text: str = html_element.text or ""
        leading_text = leading_text.replace("\n", " ").strip()
        if len(leading_text) > 0:
            layout_element.add(ChunkOfText(leading_text))  # type: ignore[union-attr]

        for e in html_element.getchildren():

            # process element
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], layout_element
            )

            # trailing text
            trailing_text: str = e.tail or ""
            trailing_text = trailing_text.replace("\n", " ").strip()
            if len(trailing_text) > 0:
                for w in trailing_text.split(" "):
                    if len(w) == 0:
                        continue
                    layout_element.add(ChunkOfText(w + " "))  # type: ignore[union-attr]
