#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of BaseTagTransformer handles <td> tags
"""
import typing
import xml.etree.ElementTree as ET

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import (
    BaseTagTransformer,
)


class TdTagTransformer(BaseTagTransformer):
    """
    This implementation of BaseTagTransformer handles <td> tags
    """

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if the html_element is a <td> element,
        False otherwise
        """
        return html_element.tag == "td"

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms a <td> tag to its corresponding LayoutElement
        """

        assert self._contains_only_text_or_single_layout_element(
            html_element
        ), "mixing text and non-text is not supported in <li> elements"

        # <td> contains a single element (that is not text)
        if html_element.text is None:
            self.get_root_tag_transformer().transform(
                html_element.getchildren()[0],
                parent_elements + [html_element],
                layout_element,
            )
            return

        chunks_of_text: HeterogeneousParagraph = HeterogeneousParagraph([])
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

        # correct spacing
        self._correct_spacing_for_chunks_of_text(chunks_of_text)

        # add to parent
        col_span: int = int(html_element.get("colspan", "1"))
        if col_span == 1:
            layout_element.add(chunks_of_text)  # type: ignore[union-attr]
        else:
            layout_element.add(TableCell(chunks_of_text, col_span=col_span))  # type: ignore[union-attr]
