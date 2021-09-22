#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <ol> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.html_to_pdf.read.transformer import (
    Transformer,
)


class OlTagTransformer(Transformer):
    """
    This implementation of BaseTagTransformer handles <ol> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <ol> element,
        False otherwise
        """
        return html_element.tag == "ol"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <ol> tag to its corresponding LayoutElement
        """
        ordered_list: OrderedList = OrderedList()

        # process children
        for e in html_element.getchildren():
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], ordered_list
            )

        # tail of html_element should be process by whoever is processing <ol>

        # add to parent
        layout_element.add(ordered_list)  # type: ignore[union-attr]
