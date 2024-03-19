#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement aggregates other LayoutElements
and lays them out on consecutive lines. If a line is full, it overflows
into the next line.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement


class InlineFlow(LayoutElement):
    """
    This implementation of LayoutElement aggregates other LayoutElements
    and lays them out on consecutive lines. If a line is full, it overflows
    into the next line.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(InlineFlow, self).__init__()
        self._content: typing.List[LayoutElement] = []

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        # all lines
        layout_lines: typing.List[typing.List[LayoutElement]] = [[]]
        layout_lines_height: typing.List[Decimal] = [Decimal(0)]

        # current line
        layout_line_width: Decimal = Decimal(0)

        # distribute content over lines
        for e in self._content:
            cbox: Rectangle = InlineFlow._get_min_content_box(e)
            w: Decimal = cbox.get_width()
            h: Decimal = cbox.get_height()
            if layout_line_width + w > available_space.get_width() or (
                e.__class__.__name__ == "LineBreakChunk"
            ):
                e._previous_layout_box = Rectangle(
                    available_space.get_x(), Decimal(0), w, h
                )
                layout_lines.append([e])
                layout_lines_height.append(h)
                layout_line_width = w
            else:
                e._previous_layout_box = Rectangle(
                    available_space.get_x() + layout_line_width, Decimal(0), w, h
                )
                layout_lines[-1].append(e)
                layout_line_width += w
                layout_lines_height[-1] = max(layout_lines_height[-1], h)

        # set height on all elements
        y: Decimal = available_space.get_y() + available_space.get_height()
        for i, line in enumerate(layout_lines):
            y -= layout_lines_height[i]
            for e in line:
                assert e._previous_layout_box is not None
                e._previous_layout_box = Rectangle(
                    e._previous_layout_box.get_x(),
                    y,
                    e._previous_layout_box.get_width(),
                    layout_lines_height[i],
                )

        # calculate total dimensions
        return Rectangle(
            available_space.get_x(),
            available_space.get_y()
            + available_space.get_height()
            - sum(layout_lines_height),
            available_space.get_width(),
            Decimal(sum(layout_lines_height)),
        )

    @staticmethod
    def _get_min_content_box(e: LayoutElement) -> Rectangle:
        r0: typing.Optional[Rectangle] = e.get_smallest_landscape_box()
        assert r0 is not None
        return r0

    def _paint_content_box(self, page: "Page", content_box: Rectangle) -> None:  # type: ignore [name-defined]
        for e in self._content:
            prev_layout_box: typing.Optional[Rectangle] = e.get_previous_layout_box()
            assert prev_layout_box is not None
            e.paint(page, prev_layout_box)

    #
    # PUBLIC
    #

    def add(self, e: LayoutElement) -> "InlineFlow":
        """
        This function adds a LayoutElement to this InlineFlow
        :param e:   the LayoutElement to be added
        :return:    self
        """

        # keep track of font size
        if len(self._content) == 0:
            try:
                self._font_size = e.get_font_size()
            except:
                pass

        if isinstance(e, InlineFlow):
            for child_e in e._content:
                self.add(child_e)
        else:
            self._content.append(e)
        return self

    def extend(self, es: typing.List[LayoutElement]) -> "InlineFlow":
        """
        This function adds a typing.List of LayoutElement(s) to this InlineFlow
        :param es:  the LayoutElements to be added
        :return:    self
        """
        for e in es:
            self.add(e)
        return self
