#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a jpeg image object
"""
import io
import logging
import typing
from typing import Any, Optional, Union

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.transformer import Transformer, ReadTransformerState
from borb.io.read.types import AnyPDFType, Name, Stream, add_base_methods
from borb.pdf.canvas.event.event_listener import EventListener
from PIL import Image  # type: ignore [import]

logger = logging.getLogger(__name__)


class CompressedJPEGImageTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a jpeg image object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed is a JPEG object
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
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a JPEG Image from a byte stream
        """
        assert isinstance(object_to_transform, Stream)

        # modify filter (temporarily)
        filters: typing.List = object_to_transform["Filter"]
        filters.pop(len(filters) - 1)

        # decode stream
        decode_stream(object_to_transform)

        # re-apply filter
        filters.append(Name("DCTDecode"))

        # use PIL to read image bytes
        assert isinstance(object_to_transform, Stream)
        raw_byte_array = object_to_transform["Bytes"]

        try:
            tmp = Image.open(io.BytesIO(raw_byte_array))
            tmp.getpixel(
                (0, 0)
            )  # attempting to read pixel 0,0 will trigger an error if the underlying image does not exist
        except:
            logger.debug(
                "Unable to read compressed jpeg image. Constructing empty image of same dimensions."
            )
            w = int(object_to_transform["Width"])
            h = int(object_to_transform["Height"])
            tmp = Image.new("RGB", (w, h), (128, 128, 128))

        # add base methods
        add_base_methods(tmp)

        # set parent
        tmp.set_parent(parent_object)

        # add event listeners
        for l in event_listeners:
            tmp.add_event_listener(l)

        # return
        return tmp
