#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base Transformer implementation.
Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
"""
import io
import typing

from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Reference
from borb.pdf.canvas.event.event_listener import EventListener


class ReadTransformerState:
    """
    This class represents all the meta-information used in the process of reading a PDF document.
    This includes:
    - the root object (the Document itself)
    - the tokenizer
    - references that have been resolved (to avoid endless loops)
    - etc
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        password: typing.Optional[str] = None,
        root_object: typing.Optional[typing.Any] = None,
        source: typing.Optional[
            typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO]
        ] = None,
        tokenizer: typing.Optional[HighLevelTokenizer] = None,
    ):
        self.indirect_reference_chain: typing.Set[Reference] = set()
        self.password: typing.Optional[str] = password
        self.root_object = root_object
        self.security_handler: typing.Optional["StandardSecurityHandler"] = None  # type: ignore[name-defined]
        self.source = source
        self.tokenizer = tokenizer

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #


class Transformer:
    """
    Base Transformer implementation.
    Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._children = []
        self._invocation_count: int = 0
        self._level: int = 0
        self._parent = None

    #
    # PRIVATE
    #

    def _is_recursive_object(self, object_to_transform) -> bool:
        try:
            p = object_to_transform
            parents = [p]
            while p is not None:
                p = p.get_parent()
                if p in parents:
                    return True
                parents.append(p)
        except:
            pass
        return False

    #
    # PUBLIC
    #

    def add_child_transformer(self, child_transformer: "Transformer") -> "Transformer":  # type: ignore[name-defined]
        """
        Add a child ReadBaseTransformer to this ReadBaseTransformer.
        Child transformers can be used to encapsulate specific object-creation/transformation logic.
        e.g. creating XREF, converting arrays, dictionaries, etc
        :param handler: the ReadBaseTransformer implementation to be added
        :type handler:  Transformer
        """
        self._children.append(child_transformer)
        child_transformer._parent = self
        return self

    def can_be_transformed(
        self,
        object: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType],
    ) -> bool:
        """
        This function returns True if the object to be transformed can be transformed by this ReadBaseTransformer
        """
        return False

    def get_children(self) -> typing.List["Transformer"]:
        """
        This functions returns all child ReadBaseTransformers of this ReadBaseTransformer
        """
        return self._children

    def get_root_transformer(self) -> "Transformer":  # type: ignore[name-defined]
        """
        This function returns the top-level ReadBaseTransformer.
        This is useful when delegating calls from inside a ReadBaseTransformer to another.
        e.g. Transforming a dictionary by reading its delimiters and then transforming each key/value in turn by
        calling top-level ReadBaseTransformer
        """
        p = self
        while p._parent is not None:
            p = p._parent
        return p

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function reads an object from a byte stream.
        The object being read depends on the implementation of ReadBaseTransformer.
        """
        if self._is_recursive_object(object_to_transform):
            return object_to_transform
        for h in self._children:
            if h.can_be_transformed(object_to_transform):
                self._level += 1
                self._invocation_count += 1
                out = h.transform(
                    object_to_transform,
                    parent_object=parent_object,
                    context=context,
                    event_listeners=event_listeners,
                )
                self._level -= 1
                return out
        return None
