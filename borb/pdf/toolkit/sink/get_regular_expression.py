#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A `Sink` implementation that extracts text matching a regular expression from a PDF.

This class processes `TextEvent` objects, reconstructs textual content per page, and
applies a specified regular expression to identify matches. For each match, metadata
such as bounding boxes, font properties, and the regex match object are stored.
"""
import collections
import typing

from borb.pdf.page_size import PageSize
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.sink.sink import Sink
from borb.pdf.toolkit.source.event.text_event import TextEvent

MatchType = collections.namedtuple(
    "MatchType", ["bounding_boxes", "font_color", "font_size", "font", "re_match"]
)


class GetRegularExpression(Sink):
    """
    A `Sink` implementation that extracts text matching a regular expression from a PDF.

    This class processes `TextEvent` objects, reconstructs textual content per page, and
    applies a specified regular expression to identify matches. For each match, metadata
    such as bounding boxes, font properties, and the regex match object are stored.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, pattern: typing.Union[str, "re.Pattern"]):  # type: ignore[name-defined]
        """
        Initialize the `GetRegularExpression` sink with a given regular expression pattern.

        This constructor sets up internal data structures to store text events and their
        corresponding matches per page. The provided pattern is compiled into a `re.Pattern`
        object if it is passed as a string.

        :param pattern: The regular expression pattern used for text extraction.
                        Can be a compiled `re.Pattern` or a string that will be compiled.
        """
        super().__init__()
        self.__events_per_page: typing.Dict[int, typing.List[TextEvent]] = {}
        self.__matches_per_page: typing.Dict[int, typing.List[MatchType]] = {}
        import re

        self.__pattern: re.Pattern = (
            pattern if isinstance(pattern, re.Pattern) else re.compile(pattern)
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_output(self) -> typing.Any:
        """
        Retrieve the aggregated results from the pipeline.

        This method should be overridden by subclasses to provide the specific output
        collected by the `Sink`. By default, it returns `None`, indicating that no
        aggregation or processing has been implemented.

        :return: The aggregated output from the pipeline, or `None` if not implemented.
        """
        return self.__matches_per_page

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        if not isinstance(event, TextEvent):
            return

        if len(event.get_text().strip()) == 0:
            return

        page_nr: int = event.get_page_nr()
        self.__events_per_page[page_nr] = self.__events_per_page.get(page_nr, []) + [
            event
        ]

        # define sort function
        def __indo_european_reading_order(e: TextEvent) -> int:
            y_upside_down: int = int(PageSize.A4_PORTRAIT[1] - e.get_y())
            # y_upside_down = y_upside_down - (y_upside_down % 12)
            return int(y_upside_down * PageSize.A4_PORTRAIT[1] + e.get_x())

        # sort
        self.__events_per_page[page_nr] = sorted(
            self.__events_per_page[page_nr],
            key=__indo_european_reading_order,
        )

        # IF there are no events
        # THEN return
        if len(self.__events_per_page[page_nr]) == 0:
            return

        # get text
        prev_x: float = self.__events_per_page[page_nr][0].get_x()
        prev_y: float = self.__events_per_page[page_nr][0].get_y()
        text: str = ""
        text_length_after_event: typing.Dict[TextEvent, int] = {}
        for e in self.__events_per_page[page_nr]:

            # IF the difference in y-coordinate is too large
            # THEN add a <newline>
            y: float = e.get_y()
            if abs(prev_y - y) > e.get_height() // 2:
                text += "\n"
                prev_y = y
                prev_x = e.get_x()

            # IF the difference in x-coordinate is too large
            # THEN add a <space>
            x: float = e.get_x()
            if abs(prev_x - x) > (0.250 * e.get_font_size()):
                text += " "

            # add text
            text += e.get_text() or ""
            text_length_after_event[e] = len(text)

            # calculate prev_x
            prev_x = e.get_x() + e.get_width()

        # get matches
        import re

        self.__matches_per_page[page_nr] = []
        for m in re.finditer(self.__pattern, text):
            event_start_index = len(
                [k for k, v in text_length_after_event.items() if v <= m.start()]
            )
            event_stop_index = len(
                [k for k, v in text_length_after_event.items() if v < m.end()]
            )

            # add match
            events: typing.List[TextEvent] = self.__events_per_page[page_nr][
                event_start_index:event_stop_index
            ]
            self.__matches_per_page[page_nr] += [
                MatchType(
                    bounding_boxes=[
                        (e.get_x(), e.get_y(), e.get_width(), e.get_height())
                        for e in events
                    ],
                    font_color=events[0].get_font_color(),
                    font_size=events[0].get_font_size(),
                    font=events[0].get_font(),
                    re_match=m,
                )
            ]
