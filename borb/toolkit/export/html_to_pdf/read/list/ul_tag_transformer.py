#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <ul> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.toolkit.export.html_to_pdf.read.transformer import Transformer


class UlTagTransformer(Transformer):
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
