#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains the basis for events and eventlisteners
"""


class Event:
    """
    This class represents a generic event
    """

    pass


class EventListener:
    """
    This class represents a generic event listener
    This listener is notified whenever the canvas processes an event/command.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def _event_occurred(self, event: Event) -> None:
        """
        This method is called whenever a matching Event is fired from the Canvas.
        EventListeners can then choose to act on those Event objects.
        :param event:   the Event that triggered this method
                        e.g. "a Page has started", "a piece of text is being rendered", etc
        :return:        None
        """
        pass
