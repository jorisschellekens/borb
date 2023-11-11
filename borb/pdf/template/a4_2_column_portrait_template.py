#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a PDF document
"""

from borb.pdf.canvas.layout.page_layout.multi_column_layout import TwoColumnLayout
from borb.pdf.document.document import Document as Document
from borb.pdf.page.page import Page
from borb.pdf.template.a4_portrait_template import A4PortraitTemplate


class A42ColumnPortraitTemplate(A4PortraitTemplate):
    """
    This class represents an A4 portrait PDF document
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__()
        self._document: Document = Document()
        self._page: Page = Page()
        self._document.add_page(self._page)
        self._layout: TwoColumnLayout = TwoColumnLayout(self._page)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
