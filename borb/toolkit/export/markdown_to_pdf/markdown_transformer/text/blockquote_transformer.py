#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles block quotes
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.toolkit.export.markdown_to_pdf.markdown_transformer.base_markdown_transformer import (
    BaseMarkdownTransformer,
    MarkdownTransformerState,
)


class BlockQuoteTransformer(BaseMarkdownTransformer):
    """
    This implementation of BaseMarkdownTransformer handles block quotes
    """

    def _can_transform(self, context: MarkdownTransformerState) -> bool:
        return context.get_markdown_string()[context.tell()] == ">" and (
            context.tell() == 0
            or context.get_markdown_string()[context.tell() - 1] == "\n"
        )

    def _transform(self, context: MarkdownTransformerState) -> None:

        end_of_input: int = self._as_long_as_input_lines_match(">.*", context)
        block_quote_lines: typing.List[str] = context.get_markdown_string()[
            context.tell() : end_of_input - 1
        ].split("\n")
        block_quote_lines = [x[2:] for x in block_quote_lines]

        # transform the markdown syntax per line
        el: HeterogeneousParagraph = HeterogeneousParagraph(
            background_color=HexColor("c3c3c3"),
            padding_top=Decimal(5),
            padding_right=Decimal(5),
            padding_bottom=Decimal(5),
            padding_left=Decimal(5),
            border_left=True,
            border_width=Decimal(3),
        )
        for line in block_quote_lines:
            sub_context: MarkdownTransformerState = MarkdownTransformerState(line)
            sub_context._document = context._document
            sub_context._parent_layout_element = el
            self.get_root()._transform(sub_context)

        for c in el._chunks_of_text:
            c._background_color = HexColor("c3c3c3")

        # add
        context.get_parent_layout_element().add(el)  # type: ignore [union-attr]

        # seek
        context.seek(end_of_input + 1)
