#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <i> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class ITagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <i> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <i> element,
        False otherwise
        """
        return html_element.tag == "i"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <i> tag to its corresponding LayoutElement
        """

        # font
        font_name: str = self._get_default_font_for_html_element(
            parent_elements + [html_element]
        )

        # leading text
        leading_text: str = html_element.text or ""
        leading_text = leading_text.strip()
        if len(leading_text) > 0:
            layout_element.add(ChunkOfText(leading_text, font=font_name))  # type: ignore[union-attr]

        for e in html_element.getchildren():

            # process element
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], layout_element
            )

            # trailing text
            trailing_text: str = e.tail or ""
            trailing_text = trailing_text.strip()
            if len(trailing_text) > 0:
                layout_element.add(ChunkOfText(trailing_text, font=font_name))  # type: ignore[union-attr]
