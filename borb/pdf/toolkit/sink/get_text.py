#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for extracting text content from PDF pages.

The `GetText` class processes PDF page content streams and collects the text content
rendered on each page. It stores the text events, grouped by page number, and allows
for easy retrieval of the extracted text content on a per-page basis. This class is
useful for applications that need to analyze or extract text from specific pages of a PDF.
"""
import typing

from borb.pdf.page_size import PageSize
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.sink.sink import Sink
from borb.pdf.toolkit.source.event.text_event import TextEvent


class GetText(Sink):
    """
    A filter class for extracting text content from PDF pages.

    The `GetText` class processes PDF page content streams and collects the text content
    rendered on each page. It stores the text events, grouped by page number, and allows
    for easy retrieval of the extracted text content on a per-page basis. This class is
    useful for applications that need to analyze or extract text from specific pages of a PDF.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the GetText filter.

        This constructor sets up the necessary structures for extracting and storing
        text content from each page of a PDF. It prepares the filter to capture
        text-related events during the PDF processing pipeline, allowing for text
        extraction based on the processed content streams.
        """
        super().__init__()
        self.__events_per_page: typing.Dict[int, typing.List[TextEvent]] = {}  # type: ignore[annotation-unchecked]
        self.__text_per_page: typing.Dict[int, str] = {}  # type: ignore[annotation-unchecked]

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
        return self.__text_per_page

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

        # append TextEvent
        page_nr: int = event.get_page_nr()
        self.__events_per_page[page_nr] = self.__events_per_page.get(page_nr, []) + [
            event
        ]

        # define sort function
        def __indo_european_reading_order(e: TextEvent) -> int:
            y_upside_down: int = int(PageSize.A4_PORTRAIT[1] - e.get_y())
            return int(y_upside_down * PageSize.A4_PORTRAIT[1] + e.get_x())

        # sort
        self.__events_per_page[page_nr] = sorted(
            self.__events_per_page[page_nr],
            key=__indo_european_reading_order,
        )

        # convert to text
        prev_x: float = self.__events_per_page[page_nr][0].get_x()
        prev_y: float = self.__events_per_page[page_nr][0].get_y()
        text: str = ""
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

            # calculate prev_x
            prev_x = e.get_x() + e.get_width()

        # store
        self.__text_per_page[page_nr] = text
