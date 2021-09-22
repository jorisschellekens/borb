#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles (alternate syntax) headings
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.markdown_to_pdf.read.transformer import (
    Transformer,
    TransformerState,
)


class AlternateSyntaxHeadingTransformer(Transformer):
    """
    This implementation of BaseMarkdownTransformer handles (alternate syntax) headings
    """

    def _can_transform(self, context: TransformerState) -> bool:
        # alternate syntax headings should start with an alpha character
        if not context.get_markdown_string()[context.tell()].isalpha():
            return False
        # headings should end with a <newline>
        next_newline_pos: int = context.get_markdown_string().find(
            "\n", context.tell() + 1
        )
        if next_newline_pos == -1:
            return False
        # the line under the heading should be all '=' or '-'
        next_next_newline_pos: int = context.get_markdown_string().find(
            "\n", next_newline_pos + 1
        )
        line_of_dashes: str = context.get_markdown_string()[
            next_newline_pos:next_next_newline_pos
        ].strip()
        return len(line_of_dashes) > 0 and (
            all([c == "=" for c in line_of_dashes])
            or all([c == "-" for c in line_of_dashes])
        )

    def _transform(self, context: TransformerState) -> None:

        # determine heading text
        next_newline_pos: int = context.get_markdown_string().find(
            "\n", context.tell() + 1
        )
        next_next_newline_pos: int = context.get_markdown_string().find(
            "\n", next_newline_pos + 1
        )
        heading_text: str = context.get_markdown_string()[
            context.tell() : next_newline_pos
        ]

        # determine heading level
        line_of_dashes: str = context.get_markdown_string()[
            next_newline_pos:next_next_newline_pos
        ].strip()
        heading_level: int = 0
        if line_of_dashes[0] == "=":
            heading_level = 0
        elif line_of_dashes[0] == "-":
            heading_level = 1

        # determine font size
        font_size: Decimal = Decimal(27)
        if heading_level == 1:
            font_size = Decimal(21)

        # add LayoutElement
        parent_layout_element: typing.Union[
            Document, Page, PageLayout, LayoutElement
        ] = context.get_parent_layout_element()
        assert isinstance(parent_layout_element, PageLayout)
        parent_layout_element.add(
            Heading(heading_text, font_size=font_size, outline_level=heading_level)
        )

        # seek
        context.seek(next_next_newline_pos + 1)
