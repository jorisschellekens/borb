#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <ul> tags
"""
import xml.etree.ElementTree as ET

import typing

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.layout_element import LayoutElement
from ptext.pdf.canvas.layout.list.unordered_list import UnorderedList
from ptext.pdf.canvas.layout.page_layout.page_layout import PageLayout
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from ptext.pdf.canvas.layout.text.heading import Heading
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class UlTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <ul> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <ul> element,
        False otherwise
        """
        return html_element.tag == "ul"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <ul> tag to its corresponding LayoutElement
        """
        unordered_list: UnorderedList = UnorderedList()

        # process children
        for e in html_element.getchildren():
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], unordered_list
            )

        # tail of html_element should be process by whoever is processing <ul>

        # add to parent
        layout_element.add(unordered_list)  # type: ignore[union-attr]
