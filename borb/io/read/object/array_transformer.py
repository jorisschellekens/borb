#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseTransformer converts a PDFArray to a List
"""
import io
import typing

from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import List
from borb.pdf.canvas.event.event_listener import EventListener


class ArrayTransformer(Transformer):
    """
    This implementation of BaseTransformer converts a PDFArray to a List
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
        This function returns True if the object to be transformed is a List
        """
        return isinstance(object, List)

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function reads a List from a byte stream
        """

        # create root object
        # fmt: off
        assert isinstance(object_to_transform, List), "object_to_transform must be of type List"
        object_to_transform.set_parent(parent_object)
        # fmt: on

        # transform child(ren)
        for i in range(0, len(object_to_transform)):
            object_to_transform[i] = self.get_root_transformer().transform(
                object_to_transform[i], object_to_transform, context, event_listeners
            )

        # return
        return object_to_transform
