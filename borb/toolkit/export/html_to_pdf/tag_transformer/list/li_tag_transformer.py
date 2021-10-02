#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <li> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import Span
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class LiTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <li> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <li> element,
        False otherwise
        """
        return html_element.tag == "li"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <li> tag to its corresponding LayoutElement
        """

        assert self._contains_only_text_or_single_layout_element(
            html_element
        ), "mixing text and non-text is not supported in <li> elements"

        # <li> contains a single element (that is not text)
        if html_element.text is None or len(html_element.text.strip()) == 0:
            self.get_root_tag_transformer().transform(
                html_element.getchildren()[0],
                parent_elements + [html_element],
                layout_element,
            )
            return

        chunks_of_text: Span = Span([])
        font_name: str = self._get_default_font_for_html_element(
            parent_elements + [html_element]
        )

        # leading text
        leading_text: str = html_element.text or ""
        leading_text = leading_text.strip()
        if len(leading_text) > 0:
            for w in leading_text.split(" "):
                chunks_of_text.add(ChunkOfText(w + " ", font=font_name))

        for e in html_element.getchildren():

            # process element
            self.get_root_tag_transformer().transform(
                e, parent_elements + [html_element], chunks_of_text
            )

            # trailing text
            trailing_text: str = e.tail or ""
            trailing_text = trailing_text.strip()
            if len(trailing_text) > 0:
                for w in trailing_text.split(" "):
                    chunks_of_text.add(ChunkOfText(w + " ", font=font_name))

        # this element should not have a tail
        assert html_element.tail is not None

        # correct spacing
        self._correct_spacing_for_chunks_of_text(chunks_of_text)

        # add to parent
        layout_element.add(chunks_of_text)  # type: ignore[union-attr]
