#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of  EventListener scans the pages of a PDF for tables.
It recognizes a table whenever a substantial amount of intersecting (or connected) horizontal/vertical lines occur.
The recognized grid must have at least 2 cells otherwise it could just be a piece of text in a box.
"""
import logging
import math
import typing
from decimal import Decimal

# fmt: off
from borb.datastructure.disjoint_set import disjointset
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.event.line_render_event import LineRenderEvent
from borb.pdf.canvas.geometry.line_segment import LineSegment
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph

# fmt: on

logger = logging.getLogger(__name__)


class TableDetectionByLines(EventListener):
    """
    This implementation of  EventListener scans the pages of a PDF for tables.
    It recognizes a table whenever a substantial amount of intersecting (or connected) horizontal/vertical lines occur.
    The recognized grid must have at least 2 cells otherwise it could just be a piece of text in a box.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._current_page_number: int = -1
        self._lines_per_page: typing.Dict[int, typing.List[LineSegment]] = {}
        self._tables_per_page: typing.Dict[int, typing.List[Table]] = {}
        self._text_render_events_per_page: typing.Dict[
            int, typing.List[ChunkOfTextRenderEvent]
        ] = {}

    #
    # PRIVATE
    #

    def _determine_number_of_rows_and_columns(
        self, lines_in_table: typing.List[LineSegment]
    ) -> typing.Tuple[int, int]:
        # keep track of unique xs / ys (to derive number of rows/cols)
        unique_xs: typing.Set[int] = set()
        unique_ys: typing.Set[int] = set()

        for l in lines_in_table:
            unique_xs.add(int(l.x0))
            unique_xs.add(int(l.x1))
            unique_ys.add(int(l.y0))
            unique_ys.add(int(l.y1))

        # determine number of rows/cols
        number_of_rows: int = len(unique_ys) - 1
        number_of_cols: int = len(unique_xs) - 1

        # return
        return number_of_rows, number_of_cols

    def _determine_table_bounding_box(
        self, lines_in_table: typing.List[LineSegment]
    ) -> Rectangle:
        # determine bounding box
        min_x: Decimal = lines_in_table[0].x0
        max_x: Decimal = lines_in_table[0].x0
        min_y: Decimal = lines_in_table[0].y0
        max_y: Decimal = lines_in_table[0].y0
        for l in lines_in_table:
            min_x = min([min_x, l.x0, l.x1])
            max_x = max([max_x, l.x0, l.x1])
            min_y = min([min_y, l.y0, l.y1])
            max_y = max([max_y, l.y0, l.y1])

        # return
        return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

    def _determine_table_cell_boundaries(
        self, lines_in_table: typing.List[LineSegment]
    ) -> Table:
        # keep track of unique xs / ys (to derive number of rows/cols)
        unique_xs: typing.Set[int] = set()
        unique_ys: typing.Set[int] = set()

        for l in lines_in_table:
            unique_xs.add(int(l.x0))
            unique_xs.add(int(l.x1))
            unique_ys.add(int(l.y0))
            unique_ys.add(int(l.y1))

        # determine number of rows and cols
        number_of_rows: int = len(unique_ys) - 1
        number_of_cols: int = len(unique_xs) - 1

        # sort unique_xs and unique_ys
        xs: typing.List[Decimal] = sorted([Decimal(x) for x in unique_xs])
        ys: typing.List[Decimal] = sorted([Decimal(y) for y in unique_ys])

        # find neighbouring cells and join wherever appropriate
        ds: disjointset = disjointset()
        for i in range(0, number_of_rows):
            for j in range(0, number_of_cols):
                ds.add((i, j))

        for c in range(0, len(xs) - 1):
            for r in range(0, len(ys) - 1):
                if c + 2 < len(xs):
                    logger.debug(
                        "attempting to merge [%d %d] with its right neighbour" % (r, c)
                    )
                    merged_with_right: Rectangle = Rectangle(
                        xs[c], ys[r], xs[c + 2] - xs[c], ys[r + 1] - ys[r]
                    )
                    if self._is_unbroken(merged_with_right):
                        logger.debug(
                            "merge [%d %d] with right [%d %d]" % (c, r, c + 1, r)
                        )
                        ds.union((r, c), (r, c + 1))

                if r + 2 < len(ys):
                    logger.debug(
                        "attempting to merge [%d %d] with its top neighbour" % (r, c)
                    )
                    merged_with_bottom: Rectangle = Rectangle(
                        xs[c], ys[r], xs[c + 1] - xs[c], ys[r + 2] - ys[r]
                    )
                    if self._is_unbroken(merged_with_bottom):
                        logger.debug(
                            "merge [%d %d] with bottom [%d %d]" % (c, r, c, r + 1)
                        )
                        ds.union((r, c), (r + 1, c))

        # extract clusters
        cells: typing.Dict[
            typing.Tuple[int, int], typing.List[typing.Tuple[int, int]]
        ] = {}
        for i in range(0, number_of_rows):
            for j in range(0, number_of_cols):
                p: typing.Tuple[int, int] = ds.find((i, j))
                if p not in cells:
                    cells[p] = []
                cells[p].append((i, j))

        # build Table
        table: Table = FlexibleColumnWidthTable(
            number_of_rows=number_of_rows, number_of_columns=number_of_cols
        )
        for _, v in cells.items():
            min_row: int = min([int_tuple[0] for int_tuple in v])
            max_row: int = max([int_tuple[0] for int_tuple in v])
            min_col: int = min([int_tuple[1] for int_tuple in v])
            max_col: int = max([int_tuple[1] for int_tuple in v])

            # check whether all areas are rectangular
            for i in range(min_col, max_col):
                for j in range(min_row, max_row):
                    assert (
                        j * number_of_rows + i
                    ) in v, "Non-rectangular area detected in table."

            # create TableCell
            tc: TableCell = TableCell(
                Paragraph(" "),
                row_span=max_row - min_row + 1,
                column_span=max_col - min_col + 1,
            )

            # set bounding_box
            tc._previous_layout_box = Rectangle(
                xs[min_col],
                ys[min_row],
                xs[max_col + 1] - xs[min_col],
                ys[max_row + 1] - ys[min_row],
            )
            tc._previous_paint_box = tc.get_previous_layout_box()

            # add to Table
            table.add(tc)

        # return
        return table

    @staticmethod
    def _dist(x0: Decimal, y0: Decimal, x1: Decimal, y1: Decimal) -> Decimal:
        return Decimal(math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2))

    def _event_occurred(self, event: Event) -> None:
        # BeginPageEvent
        if isinstance(event, BeginPageEvent):
            self._current_page_number += 1
            self._lines_per_page[self._current_page_number] = []
            self._tables_per_page[self._current_page_number] = []
            self._text_render_events_per_page[self._current_page_number] = []

        # ChunkOfTextRenderEvent
        if isinstance(event, ChunkOfTextRenderEvent):
            self._text_render_events_per_page[self._current_page_number].append(event)

        # LineRenderEvent
        if isinstance(event, LineRenderEvent):
            ls: LineSegment = event.get_line_segment()
            if abs(ls.x0 - ls.x1) > Decimal(1) and abs(ls.y0 - ls.y1) > Decimal(1):
                return
            if TableDetectionByLines._dist(ls.x0, ls.y0, ls.x1, ls.y1) < Decimal(1):
                return
            self._lines_per_page[self._current_page_number].append(
                event.get_line_segment()
            )

        # EndPageEvent
        if isinstance(event, EndPageEvent):
            ds = disjointset()
            for l in self._lines_per_page[self._current_page_number]:
                ds.add(l)
            for l0 in self._lines_per_page[self._current_page_number]:
                for l1 in self._lines_per_page[self._current_page_number]:
                    if l0 == l1:
                        continue
                    if ds.find(l0) == ds.find(l1):
                        continue

                    # two LineSegment objects share (at least) 1 point
                    # fmt: off
                    if TableDetectionByLines._dist(l0.x0, l0.y0, l1.x0, l1.y0) < Decimal(1):
                        ds.union(l0, l1)
                        continue
                    if TableDetectionByLines._dist(l0.x0, l0.y0, l1.x1, l1.y1) < Decimal(1):
                        ds.union(l0, l1)
                        continue
                    if TableDetectionByLines._dist(l0.x1, l0.y1, l1.x0, l1.y0) < Decimal(1):
                        ds.union(l0, l1)
                        continue
                    if TableDetectionByLines._dist(l0.x1, l0.y1, l1.x1, l1.y1) < Decimal(1):
                        ds.union(l0, l1)
                        continue
                    # fmt: on

                    # two LineSegment objects (A, B) such that 1 point of A lies on B
                    # fmt: off
                    if abs(l0.x0 - l0.x1) <= Decimal(1)                                             \
                        and (abs(l0.x0 - l1.x0) <= Decimal(1) or abs(l0.x0 - l1.x1) <= Decimal(1))  \
                        and abs(l1.y0 - l1.y1) <= Decimal(1)                                        \
                        and min(l0.y0, l0.y1) <= l1.y0 <= max(l0.y0, l0.y1):
                        ds.union(l0, l1)
                    if abs(l0.y0 - l0.y1) <= Decimal(1)                                             \
                        and (abs(l0.y0 - l1.y0) <= Decimal(1) or abs(l0.y0 - l1.y1) <= Decimal(1))  \
                        and abs(l1.x0 - l1.x1) <= Decimal(1)                                        \
                        and min(l0.x0, l0.x1) <= l1.x0 <= max(l0.x0, l0.x1):
                        ds.union(l0, l1)
                    # fmt: on

                    # two LineSegment objects intersect at right angle
                    # TODO

            # extract clusters
            clusters_of_lines: typing.Dict[LineSegment, typing.List[LineSegment]] = {}
            for l in ds:
                if ds.find(l) not in clusters_of_lines:
                    clusters_of_lines[ds.find(l)] = []
                clusters_of_lines[ds.find(l)].append(l)

            # process all lines per table individually
            for _, v in clusters_of_lines.items():
                r, c = self._determine_number_of_rows_and_columns(v)
                if r * c >= 2:
                    # determine table
                    table: Table = self._determine_table_cell_boundaries(v)
                    table._previous_layout_box = self._determine_table_bounding_box(v)
                    table._previous_paint_box = table.get_previous_layout_box()

                    # store
                    self._tables_per_page[self._current_page_number].append(table)

    def _is_unbroken(self, r: Rectangle) -> bool:
        r0: Rectangle = r.shrink(Decimal(1))
        r1: Rectangle = r.grow(Decimal(1))
        for l in self._lines_per_page[self._current_page_number]:
            # one of the points of the line lies outside the outer rectangle, one of the points lies inside the inner rectangle
            if r0.contains(l.x0, l.y0) and not r1.contains(l.x1, l.y1):
                return False
            if r0.contains(l.x1, l.y1) and not r1.contains(l.x0, l.y0):
                return False

            # both points of the line lie outside the inner rectangle
            if not r0.contains(l.x0, l.y0) and not r0.contains(l.x1, l.y1):
                # fmt: off
                if abs(l.x0 - l.x1) <= Decimal(1)                                                           \
                        and r0.get_x() <= l.x0 <= r0.get_x() + r0.get_width()                               \
                        and min(l.y0, l.y1) <= r.get_y() and max(l.y0, l.y1) >= r.get_y() + r.get_height():
                    return False
                if abs(l.y0 - l.y1) <= Decimal(1)                                                           \
                        and r0.get_y() <= l.y0 <= r0.get_y() + r0.get_height()                              \
                        and min(l.x0, l.x1) <= r.get_x() and max(l.x0, l.x1) >= r.get_x() + r.get_width():
                    return False
                # fmt: on

        # default
        return True

    #
    # PUBLIC
    #

    def get_table_bounding_boxes(self) -> typing.Dict[int, typing.List[Rectangle]]:
        """
        This function returns the bounding boxes (as Rectangle objects) of each Table
        that was recognized on the given page.
        """
        ZERO: Decimal = Decimal(0)
        return {
            k: [
                x.get_previous_layout_box() or Rectangle(ZERO, ZERO, ZERO, ZERO)
                for x in self._tables_per_page.get(k, [])
                if x.get_previous_layout_box() is not None
            ]
            for k in self._tables_per_page.keys()
        }

    def get_tables(self) -> typing.Dict[int, typing.List[Table]]:
        """
        This function returns each Table that was recognized on the given page.
        """
        return self._tables_per_page
