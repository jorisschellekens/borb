#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <tbody> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.toolkit.export.html_to_pdf.read.transformer import Transformer


class TBodyTagTransformer(Transformer):
    """
    This implementation of BaseTagTransformer handles <tbody> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <tbody> element,
        False otherwise
        """
        return html_element.tag == "tbody"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <tbody> tag to its corresponding LayoutElement
        """

        for e in html_element.getchildren():
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], layout_element
            )
