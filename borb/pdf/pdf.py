#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The Portable Document Format (PDF) is a file format developed by Adobe in 1993 to present documents,
    including text formatting and images, in a manner independent of application software, hardware, and operating systems.
    Based on the PostScript language, each PDF file encapsulates a complete description of a fixed-layout flat document,
    including the text, fonts, vector graphics, raster images and other information needed to display it.
    PDF was standardized as ISO 32000 in 2008, and no longer requires any royalties for its implementation.
"""
import io
import typing

# fmt: off
from borb.io.read.any_object_transformer import AnyObjectTransformer as ReadAnyObjectTransformer
from borb.io.read.transformer import ReadTransformerState
from borb.io.write.any_object_transformer import AnyObjectTransformer as WriteAnyObjectTransformer
from borb.io.write.transformer import WriteTransformerState
from borb.license.async_usage_statistics_with_fair_use_warning import AsyncUsageStatisticsWithFairUseWarning
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.document.document import Document


# fmt: on


class PDF:
    """
    The Portable Document Format (PDF) is a file format developed by Adobe in 1993 to present documents,
    including text formatting and images, in a manner independent of application software, hardware, and operating systems.
    Based on the PostScript language, each PDF file encapsulates a complete description of a fixed-layout flat document,
    including the text, fonts, vector graphics, raster images and other information needed to display it.
    PDF was standardized as ISO 32000 in 2008, and no longer requires any royalties for its implementation.

    PDF files may contain a variety of content besides flat text and graphics including logical structuring elements,
    interactive elements such as annotations and form-fields, layers, rich media (including video content),
    and three-dimensional objects using U3D or PRC, and various other data formats.

    The PDF specification also provides for encryption and digital signatures,
    file attachments, and metadata to enable workflows requiring these features.
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

    @staticmethod
    def dumps(
        file: typing.Union[io.BufferedIOBase, io.RawIOBase],
        document: Document,
    ) -> None:
        """
        This function writes a Document to a byte-stream output (which may be presented as an io.BufferedIOBase o io.RawIOBase)
        """
        AsyncUsageStatisticsWithFairUseWarning.send_usage_statistics(
            document=document, event_name="PDF.dumps"
        )
        WriteAnyObjectTransformer().transform(
            object_to_transform=document,
            context=WriteTransformerState(
                root_object=document,
                destination=file,
            ),
            destination=file,
        )

    @staticmethod
    def loads(
        file: typing.Union[io.BufferedIOBase, io.RawIOBase],
        event_listeners: typing.List[EventListener] = [],
        password: typing.Optional[str] = None,
    ) -> Document:
        """
        This function reads a byte-stream input (which may be presented as an io.BufferedIOBase o io.RawIOBase)
        and returns a Document.
        """
        document: Document = ReadAnyObjectTransformer().transform(
            file,
            parent_object=None,
            context=ReadTransformerState(password=password),
            event_listeners=event_listeners,
        )
        AsyncUsageStatisticsWithFairUseWarning.send_usage_statistics(
            document=document, event_name="PDF.loads"
        )
        return document
