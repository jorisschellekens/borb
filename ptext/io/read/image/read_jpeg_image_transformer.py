#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of ReadBaseTransformer is responsible for reading a jpeg image object
"""
import io
import typing
from typing import Optional, Any, Union

from PIL import Image  # type: ignore [import]

from ptext.io.read.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read.types import add_base_methods, Stream, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadJPEGImageTransformer(ReadBaseTransformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a jpeg image object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Stream)
            and object.get("Type", None) in ["XObject", None]
            and object.get("Subtype", None) == "Image"
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
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # use PIL to read image bytes
        assert isinstance(object_to_transform, Stream)
        raw_byte_array = object_to_transform["Bytes"]
        tmp = Image.open(io.BytesIO(raw_byte_array))

        # add base methods
        add_base_methods(tmp.__class__)

        # add hash method
        setattr(tmp.__class__, "__hash__", image_hash_method)

        # set parent
        tmp.set_parent(parent_object)

        # add event listeners
        for l in event_listeners:
            tmp.add_event_listener(l)

        # return
        return tmp


def image_hash_method(self):
    w = self.width
    h = self.height
    pixels = [
        self.getpixel((0, 0)),
        self.getpixel((0, h - 1)),
        self.getpixel((w - 1, 0)),
        self.getpixel((w - 1, h - 1)),
    ]
    hashcode = 1
    for p in pixels:
        if isinstance(p, typing.List) or isinstance(p, typing.Tuple):
            hashcode += 32 * hashcode + sum(p)
        else:
            hashcode += 32 * hashcode + p
    return hashcode
