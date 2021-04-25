# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Base Transformer implementation.
    Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
"""
import io
import typing
from typing import Optional, Any, Union

from ptext.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.io.read.types import AnyPDFType, Reference
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadTransformerContext:
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


class ReadBaseTransformer:
    """
    Base Transformer implementation.
    Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
    """

    def __init__(self):
        self.children = []
        self.parent = None
        self.level = 0
        self.invocation_count = 0

    def add_child_transformer(self, child_transformer: "ReadBaseTransformer") -> "ReadBaseTransformer":  # type: ignore[name-defined]
        """
        Add a child ReadBaseTransformer to this ReadBaseTransformer.
        Child transformers can be used to encapsulate specific object-creation/transformation logic.
        e.g. creating XREF, converting arrays, dictionaries, etc
        :param handler: the ReadBaseTransformer implementation to be added
        :type handler:  ReadBaseTransformer
        """
        self.children.append(child_transformer)
        child_transformer.parent = self
        return self

    def get_root_transformer(self) -> "ReadBaseTransformer":  # type: ignore[name-defined]
        """
        This function returns the top-level ReadBaseTransformer.
        This is useful when delegating calls from inside a ReadBaseTransformer to another.
        e.g. Transforming a dictionary by reading its delimiters and then transforming each key/value in turn by
        calling top-level ReadBaseTransformer
        """
        p = self
        while p.parent is not None:
            p = p.parent
        return p

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed can be transformed by this ReadBaseTransformer
        """
        return False

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads an object from a byte stream.
        The object being read depends on the implementation of ReadBaseTransformer.
        """
        for h in self.children:
            if h.can_be_transformed(object_to_transform):
                # print("%s<%s level='%d' invocation='%d'>" % ("   " * self.level, h.__class__.__name__, self.level, self.invocation_count), flush=True)
                self.level += 1
                self.invocation_count += 1
                out = h.transform(
                    object_to_transform,
                    parent_object=parent_object,
                    context=context,
                    event_listeners=event_listeners,
                )
                self.level -= 1
                # print("%s</%s>" % ("   " * self.level, h.__class__.__name__))
                return out
        return None
