#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <address> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class AddressTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <address> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <address> element,
        False otherwise
        """
        return html_element.tag == "address"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <address> tag to its corresponding LayoutElement
        """

        # find ITagTransformer
        i_tag_transformer: BaseTagTransformer = [
            x
            for x in self.get_root_tag_transformer().get_children()
            if x.__class__.__name__ == "ITagTransformer"
        ][0]

        # add elements
        new_layout_element: HeterogeneousParagraph = HeterogeneousParagraph()
        i_tag_transformer.transform(html_element, parent_elements, new_layout_element)

        # add element to layout
        layout_element.add(new_layout_element)  # type: ignore [union-attr]

        # tail of html_element should be process by whoever is processing <address>
