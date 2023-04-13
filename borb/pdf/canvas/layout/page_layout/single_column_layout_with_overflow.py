#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This implementation of PageLayout adds left/right/top/bottom margins to a Page
and lays out the content on the Page as if there were was a single column to flow text, images, etc into.
Once this column is full, the next page is automatically created.
"""

import copy
import typing
from decimal import Decimal

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement


class SingleColumnLayoutWithOverflow(SingleColumnLayout):
    """
    This implementation of PageLayout adds left/right/top/bottom margins to a Page
    and lays out the content on the Page as if there were was a single column to flow text, images, etc into.
    Once this column is full, the next page is automatically created.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        page: "Page",  # type: ignore [name-defined]
        horizontal_margin: typing.Optional[Decimal] = None,
        vertical_margin: typing.Optional[Decimal] = None,
    ):
        super(SingleColumnLayoutWithOverflow, self).__init__(
            page, horizontal_margin, vertical_margin
        )

    #
    # PRIVATE
    #

    @staticmethod
    def _prepare_table_for_relayout(layout_element: LayoutElement):
        from borb.pdf import Table

        assert isinstance(layout_element, Table)
        layout_element._previous_layout_box = None
        layout_element._previous_paint_box = None
        for tc in layout_element._content:
            tc._previous_layout_box = None
            tc._previous_paint_box = None
            tc._forced_layout_box = None
            tc._layout_element._previous_layout_box = None
            tc._layout_element._previous_paint_box = None

    def _split_table(
        self, layout_element: LayoutElement, available_height: Decimal
    ) -> typing.List[LayoutElement]:

        # find out at which row we ought to split the Table
        from borb.pdf import Table

        assert isinstance(layout_element, Table)
        best_row_for_split: typing.Optional[int] = None
        for i in range(0, layout_element._number_of_rows):
            if any([x._row_span != 1 for x in layout_element._get_cells_at_row(i)]):
                continue
            prev_layout_box: typing.Optional[
                Rectangle
            ] = layout_element._get_cells_at_row(i)[0].get_previous_layout_box()
            assert prev_layout_box is not None
            y: Decimal = prev_layout_box.get_y()
            if y < 0:
                continue
            if y < available_height:
                best_row_for_split = i

        # unable to split
        if best_row_for_split is None:
            assert False, (
                "%s is too tall to fit inside column / page."
                % layout_element.__class__.__name__
            )

        # first half of split
        t0 = copy.deepcopy(layout_element)
        t0._number_of_rows = best_row_for_split + 1
        t0._content = [
            x
            for x in t0._content
            if all([y[0] <= best_row_for_split for y in x._table_coordinates])
        ]
        SingleColumnLayoutWithOverflow._prepare_table_for_relayout(t0)

        # second half of split
        t1 = copy.deepcopy(layout_element)
        t1._number_of_rows = layout_element._number_of_rows - best_row_for_split - 1
        t1._content = [
            x
            for x in t1._content
            if all([y[0] > best_row_for_split for y in x._table_coordinates])
        ]
        for tc in t1._content:
            tc._table_coordinates = [
                (y - best_row_for_split - 1, x) for y, x in tc._table_coordinates
            ]
        SingleColumnLayoutWithOverflow._prepare_table_for_relayout(t1)

        # return
        return [t0, t1]

    def _split_blockflow(
        self, layout_element: LayoutElement, available_height: Decimal
    ) -> typing.List[LayoutElement]:
        from borb.pdf import BlockFlow

        assert isinstance(layout_element, BlockFlow)
        return layout_element._content

    #
    # PUBLIC
    #

    def add(self, layout_element: LayoutElement) -> "PageLayout":  # type: ignore [name-defined]
        """
        This method adds a `LayoutElement` to the current `Page`.
        """

        # anything that isn't a Table gets added as expected
        if layout_element.__class__.__name__ not in [
            "BlockFlow",
            "FlexibleColumnWidthTable",
            "FixedColumnWidthTable",
        ]:
            return super(SingleColumnLayout, self).add(layout_element)

        # previous element is used to determine the paragraph spacing
        assert self._page_height is not None
        assert self._page_width is not None
        previous_element_margin_bottom: Decimal = Decimal(0)
        previous_element_y = self._page_height - self._vertical_margin_top
        if self._previous_element is not None:
            previous_element_y = (
                self._previous_element.get_previous_layout_box().get_y()
            )
            previous_element_margin_bottom = self._previous_element.get_margin_bottom()

        # calculate next available height
        available_height: Decimal = (
            previous_element_y
            - self._vertical_margin_bottom
            - self._get_margin_between_elements(self._previous_element, layout_element)
            - max(previous_element_margin_bottom, layout_element.get_margin_top())
            - layout_element.get_margin_bottom()
        )

        # switch to new column if needed
        assert self._page_height
        if available_height < 0:
            self.switch_to_next_column()
            return self.add(layout_element)

        # ask LayoutElement to fit
        lbox: Rectangle = layout_element.get_layout_box(
            Rectangle(
                self._horizontal_margin + layout_element.get_margin_left(),
                Decimal(0),
                self._column_width
                - layout_element.get_margin_right()
                - layout_element.get_margin_left(),
                available_height,
            )
        )
        if lbox.get_height() <= available_height:
            return super(SingleColumnLayout, self).add(layout_element)

        # split Table
        if layout_element.__class__.__name__ in [
            "FlexibleColumnWidthTable",
            "FixedColumnWidthTable",
        ]:
            for t in self._split_table(layout_element, available_height):
                super(SingleColumnLayoutWithOverflow, self).add(t)

        # split BlockFlow
        if layout_element.__class__.__name__ in [
            "BlockFlow",
        ]:
            for t in self._split_blockflow(layout_element, available_height):
                super(SingleColumnLayoutWithOverflow, self).add(t)

        # return
        return self
