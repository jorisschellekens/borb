#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <th> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class ThTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <th> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <th> element,
        False otherwise
        """
        return html_element.tag == "th"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <th> tag to its corresponding LayoutElement
        """

        # find <td> worker
        td_tag_transformer: typing.Optional[BaseTagTransformer] = next(
            iter(
                [
                    x
                    for x in self.get_root_tag_transformer().get_children()
                    if x.__class__.__name__ == "TdTagTransformer"
                ]
            ),
            None,
        )
        assert td_tag_transformer is not None

        # delegate
        td_tag_transformer.transform(html_element, parent_elements, layout_element)
