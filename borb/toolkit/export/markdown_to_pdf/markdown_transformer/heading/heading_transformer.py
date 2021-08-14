#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles headings
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.markdown_to_pdf.markdown_transformer.base_markdown_transformer import (
    BaseMarkdownTransformer,
    MarkdownTransformerState,
)


class HeadingTransformer(BaseMarkdownTransformer):
    """
    This implementation of BaseMarkdownTransformer handles headings
    """

    def _can_transform(self, context: MarkdownTransformerState) -> bool:
        return context.get_markdown_string()[context.tell()] == "#"

    def _transform(self, context: MarkdownTransformerState) -> None:

        # determine heading text and level
        heading_text: str = context.get_markdown_string()[
            context.tell() : context.get_markdown_string().find("\n", context.tell())
        ]
        heading_level: int = 0
        while heading_text.startswith("#"):
            heading_text = heading_text[1:]
            heading_level += 1
        heading_level -= 1
        heading_text = heading_text.lstrip()

        # determine style
        font_size: Decimal = {
            0: Decimal(27),
            1: Decimal(21),
            2: Decimal(18),
            3: Decimal(15),
            4: Decimal(12),
            5: Decimal(12),
        }.get(heading_level, Decimal(12))

        # add LayoutElement
        parent_layout_element: typing.Union[
            Document, Page, PageLayout, LayoutElement
        ] = context.get_parent_layout_element()
        assert isinstance(parent_layout_element, PageLayout)
        parent_layout_element.add(
            Heading(heading_text, font_size=font_size, outline_level=heading_level)
        )

        # seek
        context.seek(context.get_markdown_string().find("\n", context.tell()) + 1)
