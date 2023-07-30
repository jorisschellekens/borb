#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an horizontal line across the page
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class HorizontalRule(LayoutElement):
    """
    This implementation of LayoutElement represents an horizontal line across the page
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        line_width: Decimal = Decimal(1),
        line_color: Color = HexColor("000000"),
        margin_top: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
    ):
        # fmt: off
        super(HorizontalRule, self).__init__(
            margin_top=margin_top if margin_top is not None else Decimal(5),
            margin_bottom=margin_bottom if margin_bottom is not None else Decimal(5),
        )
        # fmt: on
        self._line_width: Decimal = line_width
        self._line_color: Color = line_color

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - self._line_width,
            available_space.get_width(),
            self._line_width,
        )

    def _paint_content_box(self, page: Page, available_space: Rectangle) -> None:
        # write l operator
        rgb_color: RGBColor = self._line_color.to_rgb()
        content = " q %f %f %f RG %f %f m %f %f l s Q " % (
            float(rgb_color.red),
            float(rgb_color.green),
            float(rgb_color.blue),
            float(available_space.get_x()),
            float(
                available_space.get_y()
                + available_space.get_height()
                - self._line_width
            ),
            float(available_space.get_x() + available_space.get_width()),
            float(
                available_space.get_y()
                + available_space.get_height()
                - self._line_width
            ),
        )

        # modify content stream
        page.append_to_content_stream(content)

    #
    # PUBLIC
    #
