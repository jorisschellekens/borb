#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Pipe implementation that processes PDF events and outputs them in a structured JSON format.

This class is designed to collect events from a PDF document, such as shape fill, shape stroke, and text events,
and serialize these events into a JSON format. The events are organized by the page number of the PDF document
and saved to a specified file location.
"""
import pathlib
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
from borb.pdf.toolkit.source.event.text_event import TextEvent


class GetEventsAsJSON(Pipe):
    """
    A Pipe implementation that processes PDF events and outputs them in a structured JSON format.

    This class is designed to collect events from a PDF document, such as shape fill, shape stroke, and text events,
    and serialize these events into a JSON format. The events are organized by the page number of the PDF document
    and saved to a specified file location.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(self, where_to: typing.Union[str, pathlib.Path]):
        """
        Initialize the GetEventsAsJSON pipe.

        This constructor sets up the necessary structures to collect and organize events
        from a PDF document, such as shape fill, shape stroke, and text events, into
        a dictionary, organized by page number. The collected events will later be serialized
        into a JSON file at the specified location.
        """
        super().__init__()
        self.__events_per_page: typing.Dict[int, typing.List[Event]] = {}
        self.__where_to: pathlib.Path = (
            where_to if isinstance(where_to, pathlib.Path) else pathlib.Path(where_to)
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __event_to_json_dictionary(e: Event) -> typing.Dict[str, typing.Any]:
        # ShapeFillEvent
        if isinstance(e, ShapeFillEvent):
            return {
                "class": e.__class__.__name__,
                "color": e.get_fill_color().to_rgb_color().to_hex_str(),
                "height": e.get_height(),
                "shape": e.get_shape(),
                "width": e.get_width(),
                "x": e.get_x(),
                "y": e.get_y(),
            }
        # ShapeStrokeEvent
        if isinstance(e, ShapeStrokeEvent):
            return {
                "class": e.__class__.__name__,
                "color": e.get_stroke_color().to_rgb_color().to_hex_str(),
                "height": e.get_height(),
                "shape": e.get_shape(),
                "width": e.get_width(),
                "x": e.get_x(),
                "y": e.get_y(),
            }
        # TextEvent
        if isinstance(e, TextEvent):
            return {
                "class": e.__class__.__name__,
                "height": e.get_height(),
                "text": e.get_text(),
                "width": e.get_width(),
                "x": e.get_x(),
                "y": e.get_y(),
            }
        # default
        return {"class": e.__class__.__name__}

    #
    # PUBLIC
    #

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        # IF the event is an empty TextEvent
        # THEN return
        if isinstance(event, TextEvent) and len(event.get_text().strip()) == 0:
            return

        # append event to __events_per_page
        self.__events_per_page[event.get_page_nr()] = self.__events_per_page.get(
            event.get_page_nr(), []
        ) + [event]

        # attempt to process
        import json

        with open(self.__where_to, "w") as json_file_handle:
            json_file_handle.write(
                json.dumps(
                    {
                        k: [GetEventsAsJSON.__event_to_json_dictionary(e) for e in v]
                        for k, v in self.__events_per_page.items()
                    },
                    indent=4,
                )
            )

        # push down the pipe
        next_pipe: typing.Optional[Pipe] = self.get_next()
        if next_pipe is None:
            return
        next_pipe.process(event=event)
