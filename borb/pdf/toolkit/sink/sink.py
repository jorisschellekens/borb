#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A base class representing a terminal node in a PDF processing pipeline.

The `Sink` class is designed to act as the endpoint of a pipeline, where events
that pass through the pipeline are captured or processed. Unlike other pipes
that transform or filter events, a `Sink` collects or aggregates the results for
further use, analysis, or storage.

This class is intended to be extended to provide specific implementations
of data aggregation, such as extracting text, images, bounding boxes, or
other processed content from the pipeline.
"""
import typing

from borb.pdf.toolkit.pipe import Pipe


class Sink(Pipe):
    """
    A base class representing a terminal node in a PDF processing pipeline.

    The `Sink` class is designed to act as the endpoint of a pipeline, where events
    that pass through the pipeline are captured or processed. Unlike other pipes
    that transform or filter events, a `Sink` collects or aggregates the results for
    further use, analysis, or storage.

    This class is intended to be extended to provide specific implementations
    of data aggregation, such as extracting text, images, bounding boxes, or
    other processed content from the pipeline.
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

    def get_output(self) -> typing.Any:
        """
        Retrieve the aggregated results from the pipeline.

        This method should be overridden by subclasses to provide the specific output
        collected by the `Sink`. By default, it returns `None`, indicating that no
        aggregation or processing has been implemented.

        :return: The aggregated output from the pipeline, or `None` if not implemented.
        """
        return None
