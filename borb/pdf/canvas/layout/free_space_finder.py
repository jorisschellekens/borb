#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener keeps track of which space on a Page is available
"""
import copy
import io
import typing
from decimal import Decimal

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.event_listener import Event, EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.page.page import Page


class FreeSpaceFinder(EventListener):
    """
    This implementation of EventListener keeps track of which space on a Page is available
    """

    def __init__(self, page: Page):
        self._page_width: typing.Optional[Decimal] = page.get_page_info().get_width()
        self._page_height: typing.Optional[Decimal] = page.get_page_info().get_height()
        assert self._page_width
        assert self._page_height

        # mock Page and Canvas
        self._mock_page: Page = copy.deepcopy(page)
        self._mock_canvas: Canvas = Canvas().set_parent(self._mock_page)  # type: ignore [attr-defined]

        # grid information
        self._grid_resolution: int = 10
        self._grid: typing.List[typing.List[bool]] = []

        # render canvas
        self._render_canvas()

    def get_grid_resolution(self) -> int:
        """
        This function returns the grid resolution of the FreeSpaceFinder.
        """
        return self._grid_resolution

    def get_number_of_columns_in_grid(self) -> int:
        """
        This function returns the number of columns in the grid used by this FreeSpaceFinder
        """
        return len(self._grid[0])

    def get_number_of_rows_in_grid(self) -> int:
        """
        This function returns the number of rows in the grid used by this FreeSpaceFinder
        """
        return len(self._grid)

    def _mark_as_unavailable(self, rectangle: Rectangle):
        x_grid = int(int(rectangle.x) / self._grid_resolution)
        y_grid = int(int(rectangle.y) / self._grid_resolution)
        w = int(int(rectangle.width) / self._grid_resolution)
        h = int(int(rectangle.height) / self._grid_resolution)
        for i in range(x_grid - 1, x_grid + w + 1):
            for j in range(y_grid - 1, y_grid + h + 1):
                if i < 0 or i >= len(self._grid):
                    continue
                if j < 0 or j >= len(self._grid[i]):
                    continue
                self._grid[i][j] = False

    def _render_canvas(self):
        w = int(int(self._page_width) / self._grid_resolution)
        h = int(int(self._page_height) / self._grid_resolution)

        # mark everything as available
        for i in range(0, w):
            self._grid.append([True for x in range(0, h)])

        # add listeners
        self._mock_canvas.add_event_listener(self)

        # process canvas
        contents = self._mock_page["Contents"]
        if isinstance(contents, dict):
            CanvasStreamProcessor(self._mock_page, self._mock_canvas).read(
                io.BytesIO(contents["DecodedBytes"])
            )
        if isinstance(contents, list):
            bts = b"".join([x["DecodedBytes"] + b" " for x in contents])
            CanvasStreamProcessor(self._mock_page, self._mock_canvas).read(
                io.BytesIO(bts)
            )

    def find_free_space(self, needed_space: Rectangle) -> typing.Optional[Rectangle]:
        """
        This function returns a Rectangle (or None) of free space (no text rendering operations, no drawing operations) near the given Rectangle
        """
        w = int(int(needed_space.width) / self._grid_resolution)
        h = int(int(needed_space.height) / self._grid_resolution)
        possible_points: typing.List[typing.Tuple[Decimal, Decimal]] = []
        for i in range(0, len(self._grid) - w):
            for j in range(0, len(self._grid[i]) - h):
                is_free = True
                for k in range(0, w):
                    for l in range(0, h):
                        if not self._grid[i + k][j + l]:
                            is_free = False
                            break
                    if not is_free:
                        break
                if is_free:
                    possible_points.append(
                        (
                            Decimal(i * self._grid_resolution),
                            Decimal(j * self._grid_resolution),
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
