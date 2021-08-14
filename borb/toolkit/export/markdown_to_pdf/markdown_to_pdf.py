#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class converts Markdown to PDF
"""
from borb.pdf.document import Document
from borb.toolkit.export.markdown_to_pdf.markdown_transformer.any_markdown_transformer import (
    AnyMarkdownTransformer,
)
from borb.toolkit.export.markdown_to_pdf.markdown_transformer.base_markdown_transformer import (
    MarkdownTransformerState,
)


class MarkdownToPDF:
    """
    This class converts Markdown to PDF
    """

    @staticmethod
    def convert_markdown_to_pdf(markdown: str) -> Document:
        """
        This function converts a Markdown str to a PDF
        """
        ctx: MarkdownTransformerState = MarkdownTransformerState(markdown)
        AnyMarkdownTransformer()._transform(ctx)
        return ctx.get_document()
