import io
import typing
from typing import Optional, Any, Union

from PIL import Image   # type: ignore [import]

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import add_base_methods, Stream, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


@add_base_methods
class DefaultJPEGImageTransformer(BaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Stream)
            and object.get("Type", None) in ["XObject", None]
            and object.get("Subtype", None) == ("Image")
            and "Filter" in object
            and (
                object["Filter"] == "DCTDecode"
                or (
                    isinstance(object["Filter"], list)
                    and object["Filter"][0] == "DCTDecode"
                )
            )
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # use PIL to read image bytes
        assert isinstance(object_to_transform, Stream)
        raw_byte_array = object_to_transform["Bytes"]
        tmp = Image.open(io.BytesIO(raw_byte_array))

        # add base methods
        add_base_methods(tmp.__class__)

        # set parent
        tmp.set_parent(parent_object)

        # add event listeners
        for l in event_listeners:
            tmp.add_event_listener(l)

        # return
        return tmp
