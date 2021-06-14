#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener keeps track of which space on a Page is available
"""
import copy
import io
import typing
from decimal import Decimal

from ptext.pdf.canvas.canvas import Canvas
from ptext.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from ptext.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from ptext.pdf.canvas.event.event_listener import Event, EventListener
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page import Page


class FreeSpaceFinder(EventListener):
    """
    This implementation of EventListener keeps track of which space on a Page is available
    """

    def __init__(self, page: Page):
        self.page_width: typing.Optional[Decimal] = page.get_page_info().get_width()
        self.page_height: typing.Optional[Decimal] = page.get_page_info().get_height()
        assert self.page_width
        assert self.page_height

        # mock Page and Canvas
        self.mock_page: Page = copy.deepcopy(page)
        self.mock_canvas: Canvas = Canvas().set_parent(self.mock_page)  # type: ignore [attr-defined]

        # grid information
        self.grid_resolution: int = 10
        self.grid: typing.List[typing.List[bool]] = [[]]

        # render canvas
        self._render_canvas()

    def _mark_as_unavailable(self, rectangle: Rectangle):
        x_grid = int(int(rectangle.x) / self.grid_resolution)
        y_grid = int(int(rectangle.y) / self.grid_resolution)
        w = int(int(rectangle.width) / self.grid_resolution)
        h = int(int(rectangle.height) / self.grid_resolution)
        for i in range(x_grid - 1, x_grid + w + 1):
            for j in range(y_grid - 1, y_grid + h + 1):
                if i < 0 or i >= len(self.grid):
                    continue
                if j < 0 or j >= len(self.grid[i]):
                    continue
                self.grid[i][j] = False

    def _render_canvas(self):
        w = int(int(self.page_width) / self.grid_resolution)
        h = int(int(self.page_height) / self.grid_resolution)

        # mark everything as available
        for i in range(0, w):
            self.grid.append([True for x in range(0, h)])

        # add listeners
        self.mock_canvas.add_event_listener(self)

        # process canvas
        contents = self.mock_page["Contents"]
        if isinstance(contents, dict):
            CanvasStreamProcessor(self.mock_page, self.mock_canvas).read(
                io.BytesIO(contents["DecodedBytes"])
            )
        if isinstance(contents, list):
            bts = b"".join([x["DecodedBytes"] + b" " for x in contents])
            CanvasStreamProcessor(self.mock_page, self.mock_canvas).read(
                io.BytesIO(bts)
            )

    def find_free_space(self, needed_space: Rectangle) -> typing.Optional[Rectangle]:
        """
        This function returns a Rectangle (or None) of free space (no text rendering operations, no drawing operations) near the given Rectangle
        """
        w = int(int(needed_space.width) / self.grid_resolution)
        h = int(int(needed_space.height) / self.grid_resolution)
        possible_points: typing.List[typing.Tuple[Decimal, Decimal]] = []
        for i in range(0, len(self.grid) - w):
            for j in range(0, len(self.grid[i]) - h):
                is_free = True
                for k in range(0, w):
                    for l in range(0, h):
                        if not self.grid[i + k][j + l]:
                            is_free = False
                            break
                    if not is_free:
                        break
                if is_free:
                    possible_points.append(
                        (
                            Decimal(i * self.grid_resolution),
                            Decimal(j * self.grid_resolution),
                        )
                    )
        # find point closest to desired location
        if len(possible_points) == 0:
            return None
        min_dist = (needed_space.x - possible_points[0][0]) ** 2 + (
            needed_space.y - possible_points[0][1]
        ) ** 2
        min_dist_point = possible_points[0]
        for p in possible_points:
            d = (needed_space.x - p[0]) ** 2 + (needed_space.y - p[1]) ** 2
            if d < min_dist:
                min_dist = d
                min_dist_point = p
        # return
        return Rectangle(
            min_dist_point[0],
            min_dist_point[1],
            needed_space.width,
            needed_space.height,
        )

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, ChunkOfTextRenderEvent):
            assert isinstance(event, ChunkOfTextRenderEvent)
            bounding_box_001: typing.Optional[Rectangle] = event.get_bounding_box()
            if bounding_box_001 is not None:
                self._mark_as_unavailable(bounding_box_001)
        if isinstance(event, ImageRenderEvent):
            assert isinstance(event, ImageRenderEvent)
            bounding_box_002: typing.Optional[Rectangle] = Rectangle(
                event.get_x(), event.get_y(), event.get_width(), event.get_height()
            )
            if bounding_box_002 is not None:
                self._mark_as_unavailable(bounding_box_002)
