#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener keeps track of which space on a Page is available
"""
import typing
from decimal import Decimal
import math
import pathlib

from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.pdf import PDF


class FreeSpaceFinder(EventListener):
    """
    This implementation of EventListener keeps track of which space on a Page is available
    """

    class Grid:
        """
        This class represents a rasterized, low-res view of a Page.
        But rather than rendering instructions on this raster, each cell simply keeps track
        of whether the cell is available. This enables a quick lookup for availability of a given Rectangle.
        """

        def __init__(
            self, page_width: Decimal, page_height: Decimal, resolution: Decimal
        ):
            self._page_width = page_width
            self._page_height = page_height
            self._resolution = resolution
            self._availability: typing.List[typing.List[bool]] = [
                [True for _ in range(0, math.ceil(self._page_width / self._resolution))]
                for _ in range(0, math.ceil(self._page_height / self._resolution))
            ]

        def get_free_space(
            self, desired_rectangle: Rectangle
        ) -> typing.Optional[Rectangle]:
            """
            This function returns a Rectangle (or None) of free space (no text rendering operations, no drawing operations) near the given Rectangle
            """
            w = int(int(desired_rectangle.width) / self._resolution)
            h = int(int(desired_rectangle.height) / self._resolution)
            possible_points: typing.List[typing.Tuple[Decimal, Decimal]] = []
            for i in range(0, len(self._availability) - w):
                for j in range(0, len(self._availability[i]) - h):
                    is_free = True
                    for k in range(0, w):
                        for l in range(0, h):
                            if not self._availability[i + k][j + l]:
                                is_free = False
                                break
                        if not is_free:
                            break
                    if is_free:
                        possible_points.append(
                            (
                                Decimal(i * self._resolution),
                                Decimal(j * self._resolution),
                            )
                        )

            # find point closest to desired location
            if len(possible_points) == 0:
                return None
            min_dist = (desired_rectangle.x - possible_points[0][0]) ** 2 + (
                desired_rectangle.y - possible_points[0][1]
            ) ** 2
            min_dist_point = possible_points[0]
            for p in possible_points:
                d = (desired_rectangle.x - p[0]) ** 2 + (
                    desired_rectangle.y - p[1]
                ) ** 2
                if d < min_dist:
                    min_dist = d
                    min_dist_point = p

            # return
            return Rectangle(
                min_dist_point[0],
                min_dist_point[1],
                desired_rectangle.width,
                desired_rectangle.height,
            )

        def mark_as_unavailable(self, rectangle: Rectangle) -> "FreeSpaceFinder.Grid":
            """
            This method marks a given area in this Grid as unavailable for future content
            :param rectangle:   the Rectangle to be marked
            :return:            self
            """
            x_grid = int(int(rectangle.x) / self._resolution)
            y_grid = int(int(rectangle.y) / self._resolution)
            w = int(int(rectangle.width) / self._resolution)
            h = int(int(rectangle.height) / self._resolution)
            for i in range(x_grid - 1, x_grid + w + 1):
                for j in range(y_grid - 1, y_grid + h + 1):
                    if i < 0 or i >= len(self._availability):
                        continue
                    if j < 0 or j >= len(self._availability[i]):
                        continue
                    self._availability[i][j] = False
            return self

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._page_number: int = -1
        self._grid_per_page: typing.Dict[int, FreeSpaceFinder.Grid] = {}

    #
    # PRIVATE
    #

    def _event_occurred(self, event: Event) -> None:
        # BeginPageEvent
        if isinstance(event, BeginPageEvent):
            self._page_number += 1
            self._grid_per_page[self._page_number] = FreeSpaceFinder.Grid(
                event.get_page().get_page_info().get_width() or Decimal(0),
                event.get_page().get_page_info().get_height() or Decimal(0),
                Decimal(10),
            )

        # ChunkOfTextRenderEvent
        if isinstance(event, ChunkOfTextRenderEvent):
            assert isinstance(event, ChunkOfTextRenderEvent)
            bounding_box_001: typing.Optional[
                Rectangle
            ] = event.get_previous_layout_box()
            if bounding_box_001 is not None:
                # fmt: off
                self._grid_per_page[self._page_number].mark_as_unavailable(bounding_box_001)
                # fmt: on

        # ImageRenderEvent
        if isinstance(event, ImageRenderEvent):
            assert isinstance(event, ImageRenderEvent)
            bounding_box_002: typing.Optional[Rectangle] = Rectangle(
                event.get_x(), event.get_y(), event.get_width(), event.get_height()
            )
            if bounding_box_002 is not None:
                # fmt: off
                self._grid_per_page[self._page_number].mark_as_unavailable(bounding_box_002)
                # fmt: on

    #
    # PUBLIC
    #

    @staticmethod
    def find_free_space_for_page(
        file: pathlib.Path, page_number: int, desired_rectangle: Rectangle
    ) -> typing.Optional[Rectangle]:
        """
        This function returns the nearest (Euclidean distance)
        empty Rectangle that is at least as wide and tall as the
        desired Rectangle.
        If no such Rectangle exists, this method returns None.
        """
        l: FreeSpaceFinder = FreeSpaceFinder()
        with open(file, "rb") as pdf_file_handle:
            PDF.loads(pdf_file_handle, [l])  # type: ignore[arg-type]
        return l.get_free_space_for_page(page_number, desired_rectangle)

    def get_free_space_for_page(
        self, page_number: int, desired_rectangle: Rectangle
    ) -> typing.Optional[Rectangle]:
        """
        This function returns the nearest (euclidean distance)
        empty Rectangle that is at least as wide and tall as the
        desired Rectangle.
        If no such Rectangle exists, this method returns None.
        """
        if page_number in self._grid_per_page:
            return self._grid_per_page[page_number].get_free_space(desired_rectangle)
        return None
