#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A sink class that captures image events from the PDF content pipeline.

The `GetImages` class sits at the end of the PDF processing pipeline, serving as a sink to
capture and store any image events that pass through the pipeline. It collects image-related
data, such as image objects, their positions, and dimensions, enabling further processing or
extraction of image content from the PDF document.

This class does not alter the content stream but rather listens for image-related events
and stores them for future use or analysis.
"""
import io
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.sink.sink import Sink
from borb.pdf.toolkit.source.event.image_event import ImageEvent


class GetImages(Sink):
    """
    A sink class that captures image events from the PDF content pipeline.

    The `GetImages` class sits at the end of the PDF processing pipeline, serving as a sink to
    capture and store any image events that pass through the pipeline. It collects image-related
    data, such as image objects, their positions, and dimensions, enabling further processing or
    extraction of image content from the PDF document.

    This class does not alter the content stream but rather listens for image-related events
    and stores them for future use or analysis.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a `GetImages` instance.

        The `GetImages` class acts as a sink in the PDF processing pipeline, collecting and
        organizing image-related events (`ImageEvent`) from a PDF document. This constructor
        initializes the internal data structure used to store these events, grouped by the page
        on which they occur.
        """
        super().__init__()
        self.__events_per_page: typing.Dict[int, typing.List[ImageEvent]] = {}  # type: ignore[annotation-unchecked]

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
        # PILImageModule.Image
        try:
            import PIL.Image  # type: ignore[import-untyped, import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'Pillow' library to use the GetImages class. "
                "You can install it with 'pip install Pillow'."
            )
        return {
            k: [PIL.Image.open(io.BytesIO(i.get_image())) for i in v]  # type: ignore[arg-type]
            for k, v in self.__events_per_page.items()
        }

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        if not isinstance(event, ImageEvent):
            return

        # append ImageEvent
        self.__events_per_page[event.get_page_nr()] = self.__events_per_page.get(
            event.get_page_nr(), []
        ) + [event]
