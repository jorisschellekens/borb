import io
import logging
import typing
from typing import Optional, Any, Union

from PIL import Image  # type: ignore [import]

from ptext.io.filter.stream_decode_util import decode_stream
from ptext.io.read.image.read_jpeg_image_transformer import image_hash_method
from ptext.io.read.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from ptext.io.read.types import (
    add_base_methods,
    Reference,
    AnyPDFType,
    Stream,
)
from ptext.pdf.canvas.event.event_listener import EventListener

logger = logging.getLogger(__name__)


class ReadGrayscaleImageTransformer(ReadBaseTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Stream)
            and object.get("Type", None) in ["XObject", None]
            and object.get("Subtype", None) == ("Image")
            and "Filter" in object
            and (
                object["Filter"] == "FlateDecode"
                or (
                    isinstance(object["Filter"], list)
                    and object["Filter"][0] == "FlateDecode"
                )
            )
            and object.get("ColorSpace", None) == "DeviceGray"
        )

    def transform(
        self,
        object_to_transform: Union["io.IOBase", AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        assert isinstance(object_to_transform, Stream)

        # resolve references in stream dictionary
        xref = parent_object.get_root().get("XRef")
        for k, v in object_to_transform.items():
            if isinstance(v, Reference):
                assert context is not None
                assert context.source is not None
                assert context.tokenizer is not None
                v = xref.get_object(v, context.source, context.tokenizer)
                object_to_transform[k] = v

        grayscale_bytes = [
            x for x in decode_stream(object_to_transform)["DecodedBytes"]
        ]

        # use PIL to process image bytes
        w = int(object_to_transform["Width"])
        h = int(object_to_transform["Height"])
        tmp = Image.new("RGB", (w, h))
        for i in range(0, w):
            for j in range(0, h):
                k = i * h + j
                try:
                    c = (grayscale_bytes[k], grayscale_bytes[k], grayscale_bytes[k])
                    tmp.putpixel((i, j), value=c)
                except:
                    pass

        # add base methods
        add_base_methods(tmp.__class__)

        # add hash method
        setattr(tmp.__class__, "__hash__", image_hash_method)

        # set parent
        tmp.set_parent(parent_object)

        # add event listeners
        for l in event_listeners:
            tmp.add_event_listener(l)

        # return
        return tmp
