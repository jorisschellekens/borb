#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a grayscale image object
"""
import io
import logging
import typing

from PIL import Image as PILImageModule

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.pdf_object import PDFObject
from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.pdf.canvas.event.event_listener import EventListener

logger = logging.getLogger(__name__)


class GrayscaleImageTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a grayscale image object
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

    def can_be_transformed(
        self,
        object: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType],
    ) -> bool:
        """
        This function returns True if the object to be transformed is a grayscale Image
        :param object:  the object to be transformed
        :return:        True if the object is a grayscale Image, False otherwise
        """
        return (
            isinstance(object, Stream)
            and object.get("Type", None) in ["XObject", None]
            and object.get("Subtype", None) == ("Image")
            and "Filter" in object
            and (
                object["Filter"] == "FlateDecode"
                or (
                    isinstance(object["Filter"], list)
                    and object["Filter"][0] == "FlateDecode"
                )
            )
            and object.get("ColorSpace", None) == "DeviceGray"
        )

    def transform(
        self,
        object_to_transform: typing.Union["io.IOBase", AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms an Image Dictionary into an Image Object
        :param object_to_transform:     the Image Dictionary to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        an Image Object
        """

        # fmt: off
        assert isinstance(object_to_transform, Stream), "object_to_transform must be of type Stream"
        # fmt: on

        # resolve references in stream dictionary
        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.items():
            if isinstance(v, Reference):
                # fmt: off
                assert (context is not None), "context must be defined to read Image objects"
                assert (context.source is not None), "context.source must be defined to read Image objects"
                assert (context.tokenizer is not None), "context.tokenizer must be defined to read Image objects"
                # fmt: on
                v = xref.get_object(v, context.source, context.tokenizer)
                object_to_transform[k] = v

        grayscale_bytes = [
            x for x in decode_stream(object_to_transform)["DecodedBytes"]
        ]

        # use PIL to process image bytes
        w = int(object_to_transform["Width"])
        h = int(object_to_transform["Height"])
        tmp = PILImageModule.new("RGB", (w, h))
        for i in range(0, w):
            for j in range(0, h):
                k = i * h + j
                try:
                    c = (grayscale_bytes[k], grayscale_bytes[k], grayscale_bytes[k])
                    tmp.putpixel((i, j), value=c)
                except:
                    pass

        # add base methods
        PDFObject.add_pdf_object_methods(tmp)

        # set parent
        tmp.set_parent(parent_object)  # type: ignore[attr-defined]

        # return
        return tmp
