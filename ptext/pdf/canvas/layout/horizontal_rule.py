#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of LayoutElement represents an horizontal line across the page
"""
from decimal import Decimal

from ptext.pdf.canvas.color.color import Color, RGBColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.text.paragraph import LayoutElement
from ptext.pdf.page.page import Page


class HorizontalRule(LayoutElement):
    """
    This implementation of LayoutElement represents an horizontal line across the page
    """

    def __init__(
        self,
        line_width: Decimal = Decimal(1),
        line_color: Color = RGBColor(Decimal(0), Decimal(0), Decimal(0)),
    ):
        super(HorizontalRule, self).__init__()
        self._line_width: Decimal = line_width
        self._line_color: Color = line_color

    def _calculate_layout_box_without_padding(
        self, page: "Page", bounding_box: Rectangle  # type: ignore[name-defined]
    ) -> Rectangle:
        return Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.height - self._line_width,
            bounding_box.width,
            self._line_width,
        )

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # write l operator
        rgb_color: RGBColor = self._line_color.to_rgb()
        max_rgb: Decimal = Decimal(255)
        content = " q %f %f %f RG %f %f m %f %f l s Q " % (
            rgb_color.red / max_rgb,
            rgb_color.green / max_rgb,
            rgb_color.blue / max_rgb,
            bounding_box.x,
            bounding_box.y + bounding_box.height - self._line_width,
            bounding_box.x + bounding_box.width,
            bounding_box.y + bounding_box.height - self._line_width,
        )

        # modify content stream
        self._append_to_content_stream(page, content)

        # return
        return Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.height - self._line_width,
            bounding_box.width,
            self._line_width,
        )
