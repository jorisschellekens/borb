import io
from typing import Optional, List

from ptext.io.tokenizer.high_level_tokenizer import HighLevelTokenizer
from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_object import PDFObject


class TransformerContext:
    def __init__(
        self,
        source: Optional[io.IOBase] = None,
        tokenizer: Optional[HighLevelTokenizer] = None,
        root_object: Optional[PDFHighLevelObject] = None,
    ):
        self.source = source
        self.tokenizer = tokenizer
        self.root_object = root_object
        self.indirect_reference_chain = []


class BaseTransformer:
    """
    Base Transformer implementation.
    Add children to handle specific cases (transforming dictionaries, arrays, xref, etc)
    """

    def __init__(self):
        self.handlers = []
        self.parent = None

    def add_child_transformer(self, handler: "BaseTransformer") -> "BaseTransformer":
        """
        Add a child BaseTransformer to this BaseTransformer.
        Child transformers can be used to encapsulate specific object-creation/transformation logic.
        e.g. creating XREF, converting arrays, dictionaries, etc
        :param handler: the BaseTransformer implementation to be added
        :type handler:  BaseTransformer
        """
        self.handlers.append(handler)
        handler.parent = self
        return self

    def get_root_transformer(self) -> "BaseTransformer":
        p = self
        while p.parent is not None:
            p = p.parent
        return p

    def can_be_transformed(self, object: PDFObject) -> bool:
        return False

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:
        for h in self.handlers:
            if h.can_be_transformed(object_to_transform):
                return h.transform(
                    object_to_transform,
                    parent_object=parent_object,
                    context=context,
                    event_listeners=event_listeners,
                )
        return None
