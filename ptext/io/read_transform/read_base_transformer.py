import io
import typing
from typing import Optional, Any, Union

from ptext.io.read_transform.types import AnyPDFType
from ptext.io.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadTransformerContext:
    def __init__(
        self,
        source: Optional[Union[io.BufferedIOBase, io.RawIOBase]] = None,
        tokenizer: Optional[HighLevelTokenizer] = None,
        root_object: Optional[Any] = None,
    ):
        self.source = source
        self.tokenizer = tokenizer
        self.root_object = root_object
        self.indirect_reference_chain: typing.List[str] = []


class ReadBaseTransformer:
    """
    Base Transformer implementation.
    Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
    """

    def __init__(self):
        self.children = []
        self.parent = None

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
        p = self
        while p.parent is not None:
            p = p.parent
        return p

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return False

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        for h in self.children:
            if h.can_be_transformed(object_to_transform):
                return h.transform(
                    object_to_transform,
                    parent_object=parent_object,
                    context=context,
                    event_listeners=event_listeners,
                )
        return None
