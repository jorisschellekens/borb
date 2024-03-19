#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing List objects
"""
import logging
import typing

from PIL import Image as PILImageModule

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState

logger = logging.getLogger(__name__)


class ArrayTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing List objects
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

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is a List
        :param object:  the object to be transformed
        :return:        True if the object is a List, False otherwise
        """
        return isinstance(object, List)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a List into a byte stream
        :param object_to_transform:     the List to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) List
        """

        # fmt: off
        assert isinstance(object_to_transform, List), "object_to_transform must be of type List"
        assert (context is not None), "context must be defined in order to write Array objects."
        assert (context.destination is not None), "context.destination must be defined to write Array objects"
        # fmt: on

        # avoid resolving objects twice
        object_ref: typing.Optional[Reference] = object_to_transform.get_reference()
        if object_ref is not None and object_ref in context.resolved_references:
            assert object_ref is not None
            assert object_ref.object_number is not None
            logger.debug(
                "skip writing object %d %d R (already resolved)"
                % (object_ref.object_number, object_ref.generation_number or 0)
            )
            return

        # output value
        out_value = List()

        # objects to turn into reference
        queue: typing.List[AnyPDFType] = []
        for v in object_to_transform:
            if (
                isinstance(v, Dictionary)
                or isinstance(v, List)
                or isinstance(v, Stream)
                or isinstance(v, PILImageModule.Image)
            ) and not v.is_inline():  # type: ignore [union-attr]
                out_value.append(self.get_reference(v, context))  # type: ignore [arg-type]
                queue.append(v)  # type: ignore [arg-type]
            else:
                out_value.append(v)

        # start object if needed
        started_object = False
        if object_ref is not None:
            assert object_ref.object_number is not None
            if object_ref.object_number is not None and object_ref.byte_offset is None:
                started_object = True
                self._start_object(object_to_transform, context)
            context.resolved_references.append(object_ref)

        # write dictionary at current location
        context.destination.write(bytes("[", "latin1"))
        N = len(out_value)
        for i, v in enumerate(out_value):
            self.get_root_transformer().transform(v, context)
            if i != N - 1:
                context.destination.write(bytes(" ", "latin1"))

        # write newline if the object is not inline
        if object_to_transform.is_inline():
            context.destination.write(bytes("]", "latin1"))
        else:
            context.destination.write(bytes("]\n", "latin1"))

        # end object if needed
        if started_object:
            self._end_object(object_to_transform, context)

        for e in queue:
            self.get_root_transformer().transform(e, context)

        # return
        return out_value
