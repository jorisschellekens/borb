#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Dictionary objects
"""
import logging
import typing
from typing import Optional

from PIL.Image import Image  # type: ignore [import]

from borb.io.read.types import AnyPDFType, Dictionary, Element, List, Reference, Stream
from borb.io.write.transformer import Transformer, WriteTransformerState

logger = logging.getLogger(__name__)


class DictionaryTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Dictionary objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents an Dictionary object
        """
        return isinstance(any, Dictionary)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes a Dictionary to a byte stream
        """
        assert isinstance(object_to_transform, Dictionary)
        assert (
            context is not None
        ), "A WriteTransformerState must be defined in order to write Dictionary objects."
        assert context.destination is not None
        assert context.destination

        # avoid resolving objects twice
        object_ref: typing.Optional[Reference] = object_to_transform.get_reference()  # type: ignore [attr-defined]
        if object_ref is not None and object_ref in context.resolved_references:
            assert object_ref is not None
            assert object_ref.object_number is not None
            logger.debug(
                "skip writing object %d %d R (already resolved)"
                % (object_ref.object_number, object_ref.generation_number or 0)
            )
            return

        # output value
        out_value = Dictionary()

        # objects to turn into reference
        queue: typing.List[AnyPDFType] = []
        for k, v in object_to_transform.items():
            if (
                isinstance(v, Dictionary)
                or isinstance(v, List)
                or isinstance(v, Stream)
                or isinstance(v, Image)
                or isinstance(v, Element)
            ) and v.can_be_referenced():  # type: ignore [union-attr]
                out_value[k] = self.get_reference(v, context)
                queue.append(v)
            else:
                out_value[k] = v

        # start object if needed
        started_object = False
        if object_ref is not None:
            assert object_ref.object_number is not None
            if object_ref.object_number is not None and object_ref.byte_offset is None:
                started_object = True
                self._start_object(object_to_transform, context)
            context.resolved_references.append(object_ref)

        # write dictionary at current location
        context.destination.write(bytes("<<", "latin1"))
        N = len(out_value.items())
        for i, (k, v) in enumerate(out_value.items()):
            self.get_root_transformer().transform(k, context)
            context.destination.write(bytes(" ", "latin1"))
            self.get_root_transformer().transform(v, context)
            if i != N - 1:
                context.destination.write(bytes(" ", "latin1"))
        context.destination.write(bytes(">>\n", "latin1"))

        # end object if needed
        if started_object:
            self._end_object(object_to_transform, context)

        for e in queue:
            self.get_root_transformer().transform(e, context)

        # return
        return out_value
