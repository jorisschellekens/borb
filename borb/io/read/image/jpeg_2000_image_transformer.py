#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a jpeg2000 image object
"""
import io
import logging
import typing
from typing import Any, Optional, Union

from PIL import Image  # type: ignore [import]

from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, Stream, add_base_methods
from borb.pdf.canvas.event.event_listener import EventListener

logger = logging.getLogger(__name__)


class JPEG2000ImageTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a jpeg2000 image object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed is a JPEG2000 object
        """
        return (
            isinstance(object, dict)
            and object.get("Type", None) in ["XObject", None]
            and object.get("Subtype", None) == "Image"
            and "Filter" in object
            and (
                object["Filter"] == "JPXDecode"
                or (
                    isinstance(object["Filter"], list)
                    and object["Filter"][0] == "JPXDecode"
                )
            )
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a JPEG2000 Image from byte stream
        """

        # use PIL to read image bytes
        assert isinstance(object_to_transform, Stream)
        try:
            tmp = Image.open(io.BytesIO(object_to_transform["Bytes"]))
            tmp.getpixel(
                (0, 0)
            )  # attempting to read pixel 0,0 will trigger an error if the underlying image does not exist
        except:
            logger.debug(
                "Unable to read jpeg2000 image. Constructing empty image of same dimensions."
            )
            w = int(object_to_transform["Width"])
            h = int(object_to_transform["Height"])
            tmp = Image.new("RGB", (w, h), (128, 128, 128))

        # add base methods
        add_base_methods(tmp)

        # set parent
        tmp.set_parent(parent_object)

        # return
        return tmp
