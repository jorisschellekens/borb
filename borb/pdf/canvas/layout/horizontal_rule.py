#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an horizontal line across the page
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color, HexColor, RGBColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.text.paragraph import LayoutElement
from borb.pdf.page.page import Page


class HorizontalRule(LayoutElement):
    """
    This implementation of LayoutElement represents an horizontal line across the page
    """

    def __init__(
        self,
        line_width: Decimal = Decimal(1),
        line_color: Color = HexColor("000000"),
        margin_top: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
    ):
        super(HorizontalRule, self).__init__(
            margin_top=margin_top or Decimal(6),
            margin_bottom=margin_bottom
            or Decimal(
                6,
            ),
        )
        self._line_width: Decimal = line_width
        self._line_color: Color = line_color

    def _calculate_layout_box_without_padding(
        self, page: "Page", bounding_box: Rectangle  # type: ignore[name-defined]
    ) -> Rectangle:
        layout_box: Rectangle = Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.height - self._line_width,
            bounding_box.width,
            self._line_width,
        )
        self.set_bounding_box(layout_box)
        return layout_box

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # write l operator
        rgb_color: RGBColor = self._line_color.to_rgb()
        content = " q %f %f %f RG %f %f m %f %f l s Q " % (
            rgb_color.red,
            rgb_color.green,
            rgb_color.blue,
            bounding_box.get_x(),
            bounding_box.get_y() + bounding_box.get_height() - self._line_width,
            bounding_box.get_x() + bounding_box.get_width(),
            bounding_box.get_y() + bounding_box.get_height() - self._line_width,
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
