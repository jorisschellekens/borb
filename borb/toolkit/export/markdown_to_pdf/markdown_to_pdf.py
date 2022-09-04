#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class converts Markdown to PDF
"""

from markdown_it import MarkdownIt  # type: ignore[import]

from borb.pdf.document.document import Document
from borb.toolkit.export.html_to_pdf.html_to_pdf import HTMLToPDF


class MarkdownToPDF:
    """
    This class converts Markdown to PDF
    """

    @staticmethod
    def convert_markdown_to_pdf(markdown: str) -> Document:
        """
        This function converts a Markdown str to a PDF
        """
        html: str = MarkdownIt().enable("table").render(markdown)
        return HTMLToPDF.convert_html_to_pdf(html)
