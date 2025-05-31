#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A generic class representing an event in the PDF processing pipeline.

The `Event` class serves as a base class for various events that occur during the
rendering or processing of content within a PDF document. These events may include
actions such as shapes being stroked or filled, images being rendered, and text
being rendered. This class is designed to be extended for specific event types,
allowing for flexible and extensible handling of PDF content.

The `Event` class provides a structure for representing the details of these actions,
enabling downstream processes in the pipeline to react accordingly. As the PDF processing
framework evolves, this class can be further extended to accommodate new event types,
making it a scalable foundation for handling various content rendering operations.

Current event types include:
- ShapeStrokeEvent: Represents the event when a shape is stroked.
- ShapeFillEvent: Represents the event when a shape is filled.
- ImageEvent: Represents the event when an image is rendered.
- TextEvent: Represents the event when text is rendered.

The flexibility of this class allows for new event types to be added in the future as
needed, facilitating ongoing expansion and customization of the PDF processing pipeline.
"""
import typing

from borb.pdf.document import Document
from borb.pdf.page import Page


class Event:
    """
    A generic class representing an event in the PDF processing pipeline.

    The `Event` class serves as a base class for various events that occur during the
    rendering or processing of content within a PDF document. These events may include
    actions such as shapes being stroked or filled, images being rendered, and text
    being rendered. This class is designed to be extended for specific event types,
    allowing for flexible and extensible handling of PDF content.

    The `Event` class provides a structure for representing the details of these actions,
    enabling downstream processes in the pipeline to react accordingly. As the PDF processing
    framework evolves, this class can be further extended to accommodate new event types,
    making it a scalable foundation for handling various content rendering operations.

    Current event types include:
    - ShapeStrokeEvent: Represents the event when a shape is stroked.
    - ShapeFillEvent: Represents the event when a shape is filled.
    - ImageEvent: Represents the event when an image is rendered.
    - TextEvent: Represents the event when text is rendered.

    The flexibility of this class allows for new event types to be added in the future as
    needed, facilitating ongoing expansion and customization of the PDF processing pipeline.
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

    def get_document(self) -> Document:
        """
        Return the Document where the Event occurred.

        :return: The Document where the Event occurred.
        """
        document: typing.Optional[Document] = self.get_page().get_document()
        assert document is not None
        return document

    def get_page(self) -> Page:
        """
        Return the page where the Event occurred.

        :return: The page in the document where the Event occurred.
        """
        return None  # type: ignore[return-value]

    def get_page_nr(self) -> int:
        """
        Return the page nr where the Event occurred.

        :return: The page nr in the document where the Event occurred.
        """
        page: Page = self.get_page()
        document: Document = self.get_document()
        return next(
            iter(
                [
                    i
                    for i in range(0, document.get_number_of_pages())
                    if document.get_page(i) == page
                ]
            ),
            -1,
        )
