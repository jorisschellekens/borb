#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading Reference objects
e.g. 97 0 R
"""
import io
import logging
import typing

from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Reference
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
        self,
        object: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType],
    ) -> bool:
        """
        This function returns True if the object to be transformed is a Reference
        :param object:  the object to be transformed
        :return:        True if the object is a Reference, False otherwise
        """
        return isinstance(object, Reference)

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms a PDF reference into a (borb) Reference Object
        :param object_to_transform:     the reference to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        a Reference Object
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

        # IF the reference points to a parent object
        # THEN explicitly resolve that parent and add it to the XREF cache
        # this ensures these references are handled WITH decryption rather than simply being looked up
        # by the XREF
        matching_ref_in_xref: typing.Optional[Reference] = next(
            iter(
                [
                    r
                    for r in xref._entries
                    if r.object_number == object_to_transform.object_number
                ]
            ),
            None,
        )
        if (
            matching_ref_in_xref is not None
            and matching_ref_in_xref.parent_stream_object_number is not None
        ):
            parent_reference: Reference = Reference(
                object_number=matching_ref_in_xref.parent_stream_object_number,
                generation_number=matching_ref_in_xref.generation_number,
            )
            assert parent_reference.object_number is not None
            xref._cache[parent_reference.object_number] = self.transform(
                parent_reference,
                parent_object=parent_object,
                context=context,
                event_listeners=[],
            )

        # get referenced object from XREF
        referenced_object = xref.get_object(object_to_transform, src, tok)
        if referenced_object is None:
            return None

        # set reference on referenced object
        # this ensures we can decrypt the object if needed
        try:
            referenced_object.set_reference(object_to_transform)
        except:
            logger.debug(
                "Unable to set reference on object %s" % str(referenced_object)
            )
            pass

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

        # set reference on transformed object
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
