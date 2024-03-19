#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a jpeg image object
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
from borb.io.read.types import Name
from borb.io.read.types import Stream
from borb.pdf.canvas.event.event_listener import EventListener

logger = logging.getLogger(__name__)


class CompressedJPEGImageTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a jpeg image object
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
        This function returns True if the object to be transformed is a (compressed) JPEG Image
        :param object:  the object to be transformed
        :return:        True if the object is a compressed JPEG Image, False otherwise
        """
        return (
            isinstance(object, Stream)
            and object.get("Type", None) in ["XObject", None]
            and object.get("Subtype", None) == "Image"
            and "Filter" in object
            and (
                object["Filter"] == "DCTDecode"
                or (
                    isinstance(object["Filter"], list)
                    and len(object["Filter"]) > 1
                    and object["Filter"][-1] == "DCTDecode"
                )
            )
        )

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
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

        # modify filter (temporarily)
        filters: typing.List = object_to_transform["Filter"]
        filters.pop(len(filters) - 1)

        # decode stream
        decode_stream(object_to_transform)

        # re-apply filter
        filters.append(Name("DCTDecode"))

        # use PIL to read image bytes
        raw_byte_array = object_to_transform["Bytes"]

        try:
            tmp = PILImageModule.open(io.BytesIO(raw_byte_array))
            tmp.getpixel(
                (0, 0)
            )  # attempting to read pixel 0,0 will trigger an error if the underlying image does not exist
        except:
            logger.debug(
                "Unable to read compressed jpeg image. Constructing empty image of same dimensions."
            )
            w = int(object_to_transform["Width"])
            h = int(object_to_transform["Height"])
            tmp = PILImageModule.new("RGB", (w, h), (128, 128, 128))

        # add base methods
        PDFObject.add_pdf_object_methods(tmp)

        # set parent
        tmp.set_parent(parent_object)  # type: ignore[attr-defined]

        # return
        return tmp
