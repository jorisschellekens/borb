#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of WriteBaseTransformer is responsible for writing Stream objects
"""
import logging
import typing
from typing import Optional

from ptext.io.read.types import (
    AnyPDFType,
    Dictionary,
    Stream,
    Reference,
    List,
)
from ptext.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)

logger = logging.getLogger(__name__)


class WriteStreamTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Stream objects
    """

    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Stream)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        """
        This method writes a Stream to a byte stream
        """
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Stream)

        # start object if needed
        started_object = False
        ref = object_to_transform.get_reference()  # type: ignore [attr-defined]
        if ref is not None:
            assert isinstance(ref, Reference)
            assert ref.object_number is not None
            if ref in context.resolved_references:
                logger.debug(
                    "skip writing object %d %d R (already resolved)"
                    % (ref.object_number, ref.generation_number or 0)
                )
                return
            if ref.object_number is not None and ref.byte_offset is None:
                started_object = True
                self.start_object(object_to_transform, context)
            context.resolved_references.append(ref)

        # build stream dictionary
        stream_dictionary = Dictionary()

        # objects to turn into reference
        queue: typing.List[AnyPDFType] = []
        for k, v in object_to_transform.items():
            if k in ["Bytes", "DecodedBytes"]:
                continue
            if (
                isinstance(v, Dictionary)
                or isinstance(v, List)
                or isinstance(v, Stream)
            ) and v.can_be_referenced():  # type: ignore [union-attr]
                stream_dictionary[k] = self.get_reference(v, context)
                queue.append(v)
            else:
                stream_dictionary[k] = v

        # write stream dictionary
        self.get_root_transformer().transform(stream_dictionary, context)

        # write "stream"
        context.destination.write(bytes("stream\n", "latin1"))

        # write bytes
        context.destination.write(object_to_transform["Bytes"])

        # write "endstream"
        context.destination.write(bytes("\nendstream\n", "latin1"))

        # end object if needed
        if started_object:
            self.end_object(object_to_transform, context)

        for e in queue:
            self.get_root_transformer().transform(e, context)
