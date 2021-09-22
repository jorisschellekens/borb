#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles (indented) code snippets
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.text.chunks_of_text import (
    HeterogeneousParagraph,
    LineBreakChunk,
)
from borb.toolkit.export.markdown_to_pdf.read.transformer import (
    Transformer,
    TransformerState,
)


class IndentedCodeSnippetTransformer(Transformer):
    """
    This implementation of BaseMarkdownTransformer handles (indented) code snippets
    """

    def _can_transform(self, context: TransformerState) -> bool:
        return (
            context.get_markdown_string()[context.tell()] == " "
            and context.tell() + 1 < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + 1] == " "
            and context.tell() + 2 < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + 2] == " "
            and context.tell() + 3 < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + 3] == " "
        )

    def _transform(self, context: TransformerState) -> None:

        end_of_input: int = self._as_long_as_input_lines_match("    .*", context)
        code_snippet_lines: typing.List[str] = context.get_markdown_string()[
            context.tell() : end_of_input
        ].split("\n")
        code_snippet_lines = [x[4:] for x in code_snippet_lines]

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
            sub_context: TransformerState = TransformerState(line)
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
