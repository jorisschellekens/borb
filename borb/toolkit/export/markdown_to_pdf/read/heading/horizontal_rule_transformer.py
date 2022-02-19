#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles horizontal rules
"""
import typing

from borb.pdf.canvas.layout.horizontal_rule import HorizontalRule
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.export.markdown_to_pdf.read.transformer import (
    Transformer,
    TransformerState,
)


class HorizontalRuleTransformer(Transformer):
    """
    This implementation of BaseMarkdownTransformer handles horizontal rules
    """

    def _can_transform(self, context: TransformerState) -> bool:
        """
        To create a horizontal rule, use three or more asterisks (***), dashes (---), or underscores (___) on a line by themselves.
        """
        if context.get_markdown_string()[context.tell()] != "\n":
            return False
        markdown_str: str = context.get_markdown_string()[
            context.tell()
            + 1 : context.get_markdown_string().find("\n", context.tell() + 1)
        ]
        return any([x in markdown_str for x in ["---", "***", "___"]])

    def _transform(self, context: TransformerState) -> None:

        # add LayoutElement
        parent_layout_element: typing.Union[
            Document, Page, PageLayout, LayoutElement
        ] = context.get_parent_layout_element()
        assert isinstance(parent_layout_element, PageLayout)
        parent_layout_element.add(HorizontalRule())

        # seek
        context.seek(context.get_markdown_string().find("\n", context.tell() + 1) + 1)
