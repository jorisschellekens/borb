#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <br> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class BrTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <br> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <br> element,
        False otherwise
        """
        return html_element.tag == "br"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <br> tag to its corresponding LayoutElement
        """
        assert isinstance(layout_element, HeterogeneousParagraph)
        layout_element.add_line_break()
