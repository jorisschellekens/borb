import io
from typing import List

from ptext.object.document.document import Document
from ptext.object.pdf_high_level_object import EventListener
from ptext.tranform.default_low_level_object_transformer import (
    DefaultLowLevelObjectTransformer,
)


class PDF:
    @staticmethod
    def loads(file: io.IOBase, event_listeners: List[EventListener] = []) -> Document:
        return DefaultLowLevelObjectTransformer().transform(
            file, parent_object=None, context=None, event_listeners=event_listeners
        )
