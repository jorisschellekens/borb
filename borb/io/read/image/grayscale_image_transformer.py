#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a grayscale image object
"""
import io
import logging
import typing
from typing import Any, Optional, Union

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.transformer import Transformer, ReadTransformerState
from borb.io.read.types import AnyPDFType, Reference, Stream, add_base_methods
from borb.pdf.canvas.event.event_listener import EventListener
from PIL import Image  # type: ignore [import]

logger = logging.getLogger(__name__)


class GrayscaleImageTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a grayscale image object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed is a grayscale Image
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
        object_to_transform: Union["io.IOBase", AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a grayscale Image from a byte stream
        """

        assert isinstance(object_to_transform, Stream)

        # resolve references in stream dictionary
        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.items():
            if isinstance(v, Reference):
                assert context is not None
                assert context.source is not None
                assert context.tokenizer is not None
                v = xref.get_object(v, context.source, context.tokenizer)
                object_to_transform[k] = v

        grayscale_bytes = [
            x for x in decode_stream(object_to_transform)["DecodedBytes"]
        ]

        # use PIL to process image bytes
        w = int(object_to_transform["Width"])
        h = int(object_to_transform["Height"])
        tmp = Image.new("RGB", (w, h))
        for i in range(0, w):
            for j in range(0, h):
                k = i * h + j
                try:
                    c = (grayscale_bytes[k], grayscale_bytes[k], grayscale_bytes[k])
                    tmp.putpixel((i, j), value=c)
                except:
                    pass

        # add base methods
        add_base_methods(tmp)

        # set parent
        tmp.set_parent(parent_object)

        # add event listeners
        for l in event_listeners:
            tmp.add_event_listener(l)

        # return
        return tmp
