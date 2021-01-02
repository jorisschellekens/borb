import io
import typing
from typing import Optional, Union, Any

from ptext.io.read_transform.font.read_font_descriptor_dictionary_transformer import (
    ReadFontDescriptorDictionaryTransformer,
)
from ptext.io.read_transform.font.read_font_dictionary_transformer import (
    ReadFontDictionaryTransformer,
)
from ptext.io.read_transform.image.read_ccitt_fax_image_transformer import (
    ReadCCITTFaxImageTransformer,
)
from ptext.io.read_transform.image.read_grayscale_image_transformer import (
    ReadGrayscaleImageTransformer,
)
from ptext.io.read_transform.image.read_jbig2_image_transformer import (
    ReadJBIG2ImageTransformer,
)
from ptext.io.read_transform.image.read_jpeg_2000_image_transformer import (
    ReadJPEG2000ImageTransformer,
)
from ptext.io.read_transform.image.read_jpeg_image_transformer import (
    ReadJPEGImageTransformer,
)
from ptext.io.read_transform.object.read_array_transformer import (
    ReadArrayTransformer,
)
from ptext.io.read_transform.object.read_dictionary_transformer import (
    ReadDictionaryTransformer,
)
from ptext.io.read_transform.object.read_stream_transformer import (
    ReadStreamTransformer,
)
from ptext.io.read_transform.page.read_page_dictionary_transformer import (
    ReadPageDictionaryTransformer,
)
from ptext.io.read_transform.primitive.read_number_transformer import (
    ReadNumberTransformer,
)
from ptext.io.read_transform.primitive.read_string_transformer import (
    ReadStringTransformer,
)
from ptext.io.read_transform.read_base_transformer import (
    ReadBaseTransformer,
    TransformerContext,
)
from ptext.io.read_transform.reference.read_indirect_object_transformer import (
    DefaultIndirectObjectTransformer,
)
from ptext.io.read_transform.reference.read_reference_transformer import (
    DefaultReferenceTransformer,
)
from ptext.io.read_transform.reference.read_xref_transformer import (
    DefaultXREFTransformer,
)
from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadAnyObjectTransformer(ReadBaseTransformer):
    def __init__(self):
        super().__init__()
        self.add_child_transformer(DefaultXREFTransformer())
        # fonts
        self.add_child_transformer(ReadFontDictionaryTransformer())
        self.add_child_transformer(ReadFontDescriptorDictionaryTransformer())
        # images
        self.add_child_transformer(ReadCCITTFaxImageTransformer())
        self.add_child_transformer(ReadGrayscaleImageTransformer())
        self.add_child_transformer(ReadJBIG2ImageTransformer())
        self.add_child_transformer(ReadJPEG2000ImageTransformer())
        self.add_child_transformer(ReadJPEGImageTransformer())
        # pages
        self.add_child_transformer(ReadPageDictionaryTransformer())
        # references
        self.add_child_transformer(DefaultIndirectObjectTransformer())
        self.add_child_transformer(DefaultReferenceTransformer())
        # primitives
        self.add_child_transformer(ReadStreamTransformer())
        self.add_child_transformer(ReadStringTransformer())
        self.add_child_transformer(ReadNumberTransformer())
        # objects
        self.add_child_transformer(ReadDictionaryTransformer())
        self.add_child_transformer(ReadArrayTransformer())

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, io.IOBase)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        if context is None:
            return super().transform(
                object_to_transform,
                parent_object,
                TransformerContext(),
                event_listeners,
            )
        else:
            return super().transform(
                object_to_transform, parent_object, context, event_listeners
            )
