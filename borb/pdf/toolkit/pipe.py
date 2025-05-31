#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class representing a pipeline component for processing events.

The `Pipe` class is part of a chain-of-responsibility pattern where each `Pipe`
instance processes an `Event` object and optionally forwards it to the next
component in the chain. This modular design allows for flexible event processing,
where each step in the pipeline can handle or modify the event as needed.

The `Pipe` can be extended to implement custom behavior by overriding the `process`
method. It also supports chaining through the `set_next` method, enabling seamless
linking of multiple processing steps.
"""
import typing

from borb.pdf.toolkit.event import Event


class Pipe:
    """
    A class representing a pipeline component for processing events.

    The `Pipe` class is part of a chain-of-responsibility pattern where each `Pipe`
    instance processes an `Event` object and optionally forwards it to the next
    component in the chain. This modular design allows for flexible event processing,
    where each step in the pipeline can handle or modify the event as needed.

    The `Pipe` can be extended to implement custom behavior by overriding the `process`
    method. It also supports chaining through the `set_next` method, enabling seamless
    linking of multiple processing steps.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a new instance of the Pipe class.

        This constructor sets up the initial state of the Pipe object.
        Specifically, it initializes the `__next` attribute to `None`, which will
        later hold a reference to the next Pipe object in the chain (if applicable).
        """
        self.__next: typing.Optional[Pipe] = None  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_next(self) -> typing.Optional["Pipe"]:
        """
        Retrieve the next `Pipe` in the processing pipeline.

        :return: The next `Pipe` instance, or `None` if this is the last component in the pipeline.
        """
        return self.__next

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        pass

    def set_next(self, pipe: "Pipe") -> "Pipe":
        """
        Set the next `Pipe` in the pipeline and returns the current `Pipe` instance.

        This method enables chaining of `Pipe` instances. Once set, events processed
        by this `Pipe` can be forwarded to the next `Pipe` in the chain.

        :param pipe:    The next `Pipe` instance in the pipeline.
        :return:        The current `Pipe` instance for method chaining.
        """
        self.__next = pipe
        return self
