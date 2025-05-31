#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements a pipeline design pattern for processing PDF content.

The `Pipeline` class orchestrates a sequence of `Pipe` objects to extract, filter, or
process content from a PDF. Each `Pipe` in the pipeline can perform a specific task,
and the `Pipeline` ensures that content flows through the sequence of `Pipe` objects
in the defined order.

This class supports processing both individual `Page` objects and entire `Document`
objects, making it flexible for a variety of PDF manipulation tasks.

The first `Pipe` in the pipeline may be a `Source` object, which acts as the entry
point for processing content streams. Subsequent pipes can perform filtering,
transformation, or extraction tasks.
"""
import typing

from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.toolkit.pipe import Pipe


class Pipeline:
    """
    Implements a pipeline design pattern for processing PDF content.

    The `Pipeline` class orchestrates a sequence of `Pipe` objects to extract, filter, or
    process content from a PDF. Each `Pipe` in the pipeline can perform a specific task,
    and the `Pipeline` ensures that content flows through the sequence of `Pipe` objects
    in the defined order.

    This class supports processing both individual `Page` objects and entire `Document`
    objects, making it flexible for a variety of PDF manipulation tasks.

    The first `Pipe` in the pipeline may be a `Source` object, which acts as the entry
    point for processing content streams. Subsequent pipes can perform filtering,
    transformation, or extraction tasks.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, pipes: typing.List[Pipe]):
        """
        Initialize the `Pipeline` with a list of `Pipe` objects.

        This constructor sets up the pipeline by connecting each `Pipe` to the next one
        in the sequence. The final `Pipe` in the list has no next pipe.

        :param pipes: A list of `Pipe` objects representing the sequence of operations
                      in the pipeline.
        """
        super().__init__()
        self.__pipes: typing.List[Pipe] = pipes
        for i in range(0, len(self.__pipes) - 1):
            self.__pipes[i].set_next(self.__pipes[i + 1])

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def process(self, document_or_page: typing.Union[Document, Page]):
        """
        Process a PDF `Document` or `Page` through the pipeline.

        This method determines whether the input is a `Document` or a `Page` and processes
        the content accordingly. If the first `Pipe` in the pipeline is a `Source`, it is
        responsible for initiating the processing of content streams.

        :param document_or_page: A `Document` or `Page` object to be processed by the pipeline.
        """
        if len(self.__pipes) == 0:
            return None

        from borb.pdf.toolkit.source.operator.source import Source

        source: typing.Optional[Source] = None
        if isinstance(self.__pipes[0], Source):
            source = self.__pipes[0]
        if source is None:
            return

        # IF document_or_page is a Document
        # THEN iterate over all Page object(s) in the Document
        from borb.pdf.toolkit.source.event.end_page_event import EndPageEvent

        if isinstance(document_or_page, Document):
            for i in range(0, document_or_page.get_number_of_pages()):
                page: Page = document_or_page.get_page(i)
                source.process_page(page=page)
                source.process(EndPageEvent(page=page))

        # IF document_or_page is a Page
        # THEN process the Page
        if isinstance(document_or_page, Page):
            source.process_page(page=document_or_page)
            source.process(EndPageEvent(page=document_or_page))

        # IF the final element in the Pipe is a sink
        # THEN get its output
        from borb.pdf.toolkit.sink.sink import Sink

        if isinstance(self.__pipes[-1], Sink):
            return self.__pipes[-1].get_output()

        # default
        return None
