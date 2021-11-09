#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class converts Markdown to PDF
"""
from borb.pdf.document import Document
from borb.toolkit.export.markdown_to_pdf.read.any_markdown_transformer import (
    AnyMarkdownTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.transformer import TransformerState


class MarkdownToPDF:
    """
    This class converts Markdown to PDF
    """

    @staticmethod
    def convert_markdown_to_pdf(markdown: str) -> Document:
        """
        This function converts a Markdown str to a PDF
        """
        ctx: TransformerState = TransformerState(markdown)
        AnyMarkdownTransformer()._transform(ctx)
        return ctx.get_document()
