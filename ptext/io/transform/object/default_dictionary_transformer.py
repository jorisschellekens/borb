import io
import typing
from typing import Optional, Any, Union

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import Dictionary, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultDictionaryTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFDictionary to a Dictionary
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, dict)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # create root object
        tmp = Dictionary()
        tmp.set_parent(parent_object)

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # transform key/value pair(s)
        assert isinstance(object_to_transform, Dictionary)
        for k, v in object_to_transform.items():
            v = self.get_root_transformer().transform(v, tmp, context, [])
            if v is not None:
                tmp[k] = v

        # return
        return tmp
