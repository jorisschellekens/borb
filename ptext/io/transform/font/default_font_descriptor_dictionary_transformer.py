import io
import typing
from typing import Optional, Any, Union

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.object.default_dictionary_transformer import (
    DefaultDictionaryTransformer,
)
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener
from ptext.pdf.canvas.font.font import Font


class DefaultFontDescriptorDictionaryTransformer(BaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, dict)
            and "Type" in object
            and object["Type"] == "FontDescriptor"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # convert like regular dictionary
        if isinstance(parent_object, Font):
            for t in self.get_root_transformer().handlers:
                if isinstance(t, DefaultDictionaryTransformer):
                    return t.transform(
                        object_to_transform, parent_object, context, event_listeners
                    )

        # build intermittent Font object
        tmp = Font().set_parent(parent_object) # type: ignore [attr-defined]

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        tmp["FontDescriptor"] = self.get_root_transformer().transform(
            object_to_transform, tmp, context, []
        )

        # return
        return tmp
