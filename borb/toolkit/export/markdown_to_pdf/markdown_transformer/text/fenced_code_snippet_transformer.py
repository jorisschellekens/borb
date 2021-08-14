#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles (fenced) code snippets
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.text.chunks_of_text import (
    HeterogeneousParagraph,
    LineBreakChunk,
)
from borb.toolkit.export.markdown_to_pdf.markdown_transformer.base_markdown_transformer import (
    BaseMarkdownTransformer,
    MarkdownTransformerState,
)


class FencedCodeSnippetTransformer(BaseMarkdownTransformer):
    """
    This implementation of BaseMarkdownTransformer handles (fenced) code snippets
    """

    def _can_transform(self, context: MarkdownTransformerState) -> bool:
        return (
            context.get_markdown_string()[context.tell()] == "`"
            and context.tell() + 1 < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + 1] == "`"
            and context.tell() + 2 < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + 2] == "`"
            and context.tell() + 3 < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + 3] == "\n"
        )

    def _transform(self, context: MarkdownTransformerState) -> None:

        end_of_input: int = context.get_markdown_string().find(
            "```", context.tell() + 1
        )
        code_snippet_lines: typing.List[str] = context.get_markdown_string()[
            context.tell() : end_of_input
        ].split("\n")
        code_snippet_lines = code_snippet_lines[1:-1]

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

        for line in code_snippet_lines:
            sub_context: MarkdownTransformerState = MarkdownTransformerState(line)
            sub_context._document = context._document
            sub_context._parent_layout_element = el
            self.get_root()._transform(sub_context)
            el.add(LineBreakChunk())

        for c in el._chunks_of_text:
            c._background_color = HexColor("c3c3c3")

        # add
        context.get_parent_layout_element().add(el)  # type: ignore [union-attr]

        # seek
        context.seek(end_of_input + 1)
