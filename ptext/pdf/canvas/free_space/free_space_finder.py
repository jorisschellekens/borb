import copy
import io
import typing

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.canvas import Canvas
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.canvas.event.text_render_event import TextRenderEvent
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page import Page


class FreeSpaceFinder(EventListener):
    def __init__(self, page: Page):
        self.page = copy.deepcopy(page)
        self.grid_resolution = 10
        self.mock_canvas = Canvas().set_parent(self.page)  # type: ignore [attr-defined]
        self.grid: typing.List[typing.List[bool]] = [[]]
        self._draw_text_and_objects()

    def _mark_as_unavailable(self, rectangle: Rectangle):
        x_grid = int(int(rectangle.x) / self.grid_resolution)
        y_grid = int(int(rectangle.y) / self.grid_resolution)
        w = int(int(rectangle.width) / self.grid_resolution)
        h = int(int(rectangle.height) / self.grid_resolution)
        for i in range(x_grid, x_grid + w):
            for j in range(y_grid, y_grid + h):
                if i < 0 or i >= len(self.grid):
                    continue
                if j < 0 or j >= len(self.grid[i]):
                    continue
                self.grid[i][j] = False

    def _draw_text_and_objects(self):
        w = int(int(self.page.get_page_info().get_width()) / self.grid_resolution)
        h = int(int(self.page.get_page_info().get_height()) / self.grid_resolution)

        # mark everything as available
        for i in range(0, w):
            self.grid.append([True for x in range(0, h)])

        # add listeners
        self.mock_canvas.add_listener(self)

        # process canvas
        contents = self.page["Contents"]
        if isinstance(contents, dict):
            self.mock_canvas.read(io.BytesIO(contents["DecodedBytes"]))
        if isinstance(contents, list):
            bts = b"".join([x["DecodedBytes"] + b" " for x in contents])
            self.mock_canvas.read(io.BytesIO(bts))

    def find_free_space(self, needed_space: Rectangle) -> typing.Optional[Rectangle]:
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

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, TextRenderEvent):
            assert isinstance(event, TextRenderEvent)
            space = Rectangle(
                event.get_baseline().x0,
                event.get_baseline().y0,
                event.get_baseline().x1,
                Decimal(12),
            )  # TODO: height
            self._mark_as_unavailable(space)
