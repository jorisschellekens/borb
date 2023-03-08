#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading Reference objects
e.g. 97 0 R
"""
import io
import logging
import typing
from typing import Any, Optional, Union

from borb.io.read.transformer import ReadTransformerState, Transformer
from borb.io.read.types import AnyPDFType, Reference
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.xref.xref import XREF

logger = logging.getLogger(__name__)


class ReferenceTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading Reference objects
    e.g. 97 0 R
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(ReferenceTransformer, self).__init__()
        self._cache: typing.Dict[Reference, AnyPDFType] = {}
        self._cache_hits: int = 0
        self._cache_fails: int = 0

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be converted represents a Reference
        """
        return isinstance(object, Reference)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a Reference from a byte stream
        """
        # fmt: off
        assert isinstance(object_to_transform, Reference), "object_to_transform must be of type Reference"
        # fmt: on

        # check for circular reference
        assert context is not None
        if object_to_transform in context.indirect_reference_chain:
            return None

        # lookup in cache
        ref_from_cache = self._cache.get(object_to_transform, None)
        if ref_from_cache is not None:
            self._cache_hits += 1

            # check linkage
            if ref_from_cache.get_parent() is None:
                ref_from_cache.set_parent(parent_object)
                return ref_from_cache

            # copy because of linkage
            if ref_from_cache.get_parent() != parent_object:
                ref_from_cache_copy = ref_from_cache  # TODO
                ref_from_cache_copy.set_parent(parent_object)
                return ref_from_cache_copy

        self._cache_fails += 1
        logger.debug(
            "ref. cache hits: %d, fails: %d, ratio %f"
            % (
                self._cache_hits,
                self._cache_fails,
                self._cache_hits / (self._cache_hits + self._cache_fails),
            )
        )

        # lookup xref
        # fmt: off
        assert (context.root_object is not None), "context.root_object must be defined to read Reference objects"
        assert context.root_object["XRef"] is not None, "XREF must be defined to read Reference objects"
        assert isinstance(context.root_object["XRef"], XREF), "XREF must be defined to read Reference objects"
        assert (context.tokenizer is not None), "context.tokenizer must be defined to read Reference objects"
        assert (context.source is not None), "context.source must be defined to read Reference objects"
        # fmt: on

        xref = context.root_object["XRef"]
        src = context.source
        tok = context.tokenizer

        # get reference
        referenced_object = xref.get_object(object_to_transform, src, tok)
        if referenced_object is None:
            return None

        # transform
        assert referenced_object is not None
        context.indirect_reference_chain.add(object_to_transform)
        transformed_referenced_object = self.get_root_transformer().transform(
            referenced_object, parent_object, context, event_listeners
        )
        context.indirect_reference_chain.remove(object_to_transform)

        # update cache
        if transformed_referenced_object is not None:
            self._cache[object_to_transform] = transformed_referenced_object

        # set reference
        try:
            transformed_referenced_object.set_reference(object_to_transform)
        except:
            logger.debug(
                "Unable to set reference on object %s"
                % str(transformed_referenced_object)
            )
            pass

        # return
        return transformed_referenced_object
