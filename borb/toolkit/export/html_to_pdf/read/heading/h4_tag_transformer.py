#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <h4> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.heading import Heading
from borb.toolkit.export.html_to_pdf.read.transformer import Transformer


class H4TagTransformer(Transformer):
    """
    This implementation of BaseTagTransformer handles <h4> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <h4> element,
        False otherwise
        """
        return html_element.tag == "h4"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <h4> tag to its corresponding LayoutElement
        """
        assert html_element.text is not None, "<h4> should have text"
        assert (
            len(html_element.getchildren()) == 0
        ), "<h4> children are currently not supported"
        layout_element.add(  # type: ignore[union-attr]
            Heading(html_element.text, font="Helvetica-Bold", font_size=Decimal(16))
        )
