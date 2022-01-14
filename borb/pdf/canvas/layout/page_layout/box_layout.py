#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of PageLayout adds left/right/top/bottom margins to a Page
and lays out the content on the Page as if there were multiple  boxes to flow text, images, etc into.
Once a box is full, the next box is automatically selected, although the next column can be manually selected.
"""
import typing

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.page.page import Page


class BoxLayout(PageLayout):
    """
    This implementation of PageLayout adds left/right/top/bottom margins to a Page
    and lays out the content on the Page as if there were multiple  boxes to flow text, images, etc into.
    Once a box is full, the next box is automatically selected, although the next column can be manually selected.
    """

    def __init__(self, page: Page, boxes: typing.List[Rectangle]):
        super(BoxLayout, self).__init__(page)
        assert len(boxes) > 0
        self._boxes: typing.List[Rectangle] = boxes

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        """
        This method adds a `LayoutElement` to the current `Page`.
        """
        return self
