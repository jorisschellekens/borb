#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a jpeg image object
"""
import io
import logging
import typing

from PIL import Image as PILImageModule

from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import PDFObject
from borb.io.read.types import Stream
from borb.pdf.canvas.event.event_listener import EventListener

logger = logging.getLogger(__name__)


class JPEGImageTransformer(Transformer):
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
        This function returns True if the object to be transformed is a JPEG Image
        :param object:  the object to be transformed
        :return:        True if the object is a JPEG Image, False otherwise
        """
        return (
            isinstance(object, Stream)
            and object.get("Type", None) in ["XObject", None]
            and object.get("Subtype", None) in ["Image", None]
            and "Filter" in object
            and (
                object["Filter"] == "DCTDecode"
                or (
                    isinstance(object["Filter"], list)
                    and object["Filter"][0] == "DCTDecode"
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

        # use PIL to read image bytes
        # fmt: off
        assert isinstance(object_to_transform, Stream), "object_to_transform must be of type Stream"
        # fmt: on

        # warnings
        if object_to_transform.get("Type", None) is None:
            logger.debug("Image object did not specify /Type /XObject.")
        if object_to_transform.get("Subtype", None) is None:
            logger.debug("Image object did not specify /Subtype /Image.")

        # read a pixel
        try:
            tmp = PILImageModule.open(io.BytesIO(object_to_transform["Bytes"]))
            tmp.getpixel(
                (0, 0)
            )  # attempting to read pixel 0,0 will trigger an error if the underlying image does not exist
        except:
            logger.debug(
                "Unable to read jbig2 image. Constructing empty image of same dimensions."
            )
            w: int = int(object_to_transform["Width"])
            h: int = int(object_to_transform["Height"])
            tmp = PILImageModule.new("RGB", (w, h), (128, 128, 128))

        # add base methods
        PDFObject.add_pdf_object_methods(tmp)

        # set parent
        tmp.set_parent(parent_object)  # type: ignore[attr-defined]

        # return
        return tmp
