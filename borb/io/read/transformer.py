# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base Transformer implementation.
Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
"""
import io
import typing
from typing import Any, Optional, Union

from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.types import AnyPDFType, Reference
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

    def __init__(
        self,
        source: Optional[Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO]] = None,
        tokenizer: Optional[HighLevelTokenizer] = None,
        root_object: Optional[Any] = None,
    ):
        self.source = source
        self.tokenizer = tokenizer
        self.root_object = root_object
        self.indirect_reference_chain: typing.Set[Reference] = set()


class Transformer:
    """
    Base Transformer implementation.
    Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
    """

    def __init__(self):
        self._children = []
        self._parent = None
        self._level = 0
        self._invocation_count = 0

    def get_children(self) -> typing.List["Transformer"]:
        """
        This functions returns all child ReadBaseTransformers of this ReadBaseTransformer
        """
        return self._children

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

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed can be transformed by this ReadBaseTransformer
        """
        return False

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

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads an object from a byte stream.
        The object being read depends on the implementation of ReadBaseTransformer.
        """
        if self._is_recursive_object(object_to_transform):
            return object_to_transform
        for h in self._children:
            if h.can_be_transformed(object_to_transform):
                # print("%s<%s level='%d' invocation='%d'>" % ("   " * self.level, h.__class__.__name__, self.level, self.invocation_count), flush=True)
                self._level += 1
                self._invocation_count += 1
                out = h.transform(
                    object_to_transform,
                    parent_object=parent_object,
                    context=context,
                    event_listeners=event_listeners,
                )
                self._level -= 1
                # print("%s</%s>" % ("   " * self.level, h.__class__.__name__))
                return out
        return None
