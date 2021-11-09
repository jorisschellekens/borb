#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <code> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.toolkit.export.html_to_pdf.read.transformer import Transformer


class CodeTagTransformer(Transformer):
    """
    This implementation of BaseTagTransformer handles <code> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <code> element,
        False otherwise
        """
        return html_element.tag == "code"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <code> tag to its corresponding LayoutElement
        """
        assert all(
            [self._contains_only_text_children(x) for x in html_element.getchildren()]
        )

        # font
        # TODO: verify what happens (in browsers) when you wrap <code> in <b>, <i>, <em>, etc
        font_name: str = self._get_default_font_for_html_element(
            parent_elements + [html_element]
        )

        assert html_element.text is not None
        chunks_of_text: HeterogeneousParagraph = HeterogeneousParagraph([])
        chunks_of_text.add(ChunkOfText(html_element.text, font=font_name))

        for e in html_element.getchildren():
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], chunks_of_text
            )

        # change font and background color
        for c in chunks_of_text._chunks_of_text:
            c._background_color = HexColor("#EEEEEE")
            c._font = StandardType1Font("Courier")

        # correct spacing
        self._correct_spacing_for_chunks_of_text(chunks_of_text)

        # add to parent
        layout_element.add(chunks_of_text)  # type: ignore [union-attr]
