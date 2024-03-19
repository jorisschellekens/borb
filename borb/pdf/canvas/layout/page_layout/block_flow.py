#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement aggregates other LayoutElements
and lays them out underneath each other.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement


class BlockFlow(LayoutElement):
    """
    This implementation of LayoutElement aggregates other LayoutElements
    and lays them out underneath each other.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(BlockFlow, self).__init__()
        self._content: typing.List[LayoutElement] = []

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        tallest_y_coordinate: Decimal = (
            available_space.get_y() + available_space.get_height()
        )
        if len(self._content) > 0:
            tallest_y_coordinate -= self._content[0].get_margin_top()
            tallest_y_coordinate = max(tallest_y_coordinate, Decimal(0))
        for i, e in enumerate(self._content):
            lbox: Rectangle = e.get_layout_box(
                Rectangle(
                    available_space.get_x(),
                    available_space.get_y(),
                    available_space.get_width(),
                    max(tallest_y_coordinate - available_space.get_y(), Decimal(0)),
                )
            )
            tallest_y_coordinate = lbox.get_y()
            if (i + 1) < len(self._content):
                margin: Decimal = max(
                    e.get_margin_bottom(), self._content[i + 1].get_margin_top()
                )
                tallest_y_coordinate -= margin
            else:
                tallest_y_coordinate -= e.get_margin_bottom()

        # return
        return Rectangle(
            available_space.get_x(),
            tallest_y_coordinate,
            available_space.get_width(),
            max(
                available_space.get_y()
                + available_space.get_height()
                - tallest_y_coordinate,
                Decimal(0),
            ),
        )

    def _paint_content_box(self, page: "Page", content_box: Rectangle) -> None:  # type: ignore[name-defined]
        tallest_y_coordinate: Decimal = content_box.get_y() + content_box.get_height()
        if len(self._content) > 0:
            tallest_y_coordinate -= self._content[0].get_margin_top()
            tallest_y_coordinate = max(tallest_y_coordinate, Decimal(0))
        for i, e in enumerate(self._content):
            e.paint(
                page,
                Rectangle(
                    content_box.get_x(),
                    content_box.get_y(),
                    content_box.get_width(),
                    max(tallest_y_coordinate - content_box.get_y(), Decimal(0)),
                ),
            )
            e_previous_paint_box: typing.Optional[
                Rectangle
            ] = e.get_previous_paint_box()
            assert e_previous_paint_box is not None
            tallest_y_coordinate = e_previous_paint_box.get_y()
            if (i + 1) < len(self._content):
                margin: Decimal = max(
                    e.get_margin_bottom(), self._content[i + 1].get_margin_top()
                )
                tallest_y_coordinate -= margin
            else:
                tallest_y_coordinate -= e.get_margin_bottom()

    #
    # PUBLIC
    #

    def add(self, e: LayoutElement) -> "BlockFlow":
        """
        This function adds a LayoutElement to this BlockFlow
        :param e:   the LayoutElement to be added
        :return:    self
        """

        # keep track of font size
        if len(self._content) == 0:
            try:
                self._font_size = e.get_font_size()
            except:
                pass

        # if the last element of this BlockFlow is an InlineFlow
        # and the new element is also an InlineFlow, just add the two together
        if (
            len(self._content) > 0
            and self._content[-1].__class__.__name__ == "InlineFlow"
            and e.__class__.__name__ == "InlineFlow"
        ):
            self._content[-1].add(e)  # type: ignore[attr-defined]
            return self
        # default behaviour
        self._content.append(e)
        # return
        return self

    def extend(self, es: typing.List[LayoutElement]) -> "BlockFlow":
        """
        This function adds a typing.List of LayoutElement(s) to this BlockFlow
        :param es:  the LayoutElements to be added
        :return:    self
        """
        for e in es:
            self.add(e)
        return self
