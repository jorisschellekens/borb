import io
import typing
from typing import Optional, Union, Any

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.font.default_font_descriptor_dictionary_transformer import (
    DefaultFontDescriptorDictionaryTransformer,
)
from ptext.io.transform.font.default_font_dictionary_transformer import (
    DefaultFontDictionaryTransformer,
)
from ptext.io.transform.image.default_ccitt_fax_image_transformer import (
    DefaultCCITTFaxImageTransformer,
)
from ptext.io.transform.image.default_dctdecode_image_transformer import (
    DefaultDCTDecodeImageTransformer,
)
from ptext.io.transform.image.default_grayscale_image_transformer import (
    DefaultGrayscaleImageTransformer,
)
from ptext.io.transform.image.default_jbig2_image_transformer import (
    DefaultJBIG2ImageTransformer,
)
from ptext.io.transform.image.default_jpeg_2000_image_transformer import (
    DefaultJPEG2000ImageTransformer,
)
from ptext.io.transform.image.default_jpeg_image_transformer import (
    DefaultJPEGImageTransformer,
)
from ptext.io.transform.object.default_array_transformer import DefaultArrayTransformer
from ptext.io.transform.object.default_dictionary_transformer import (
    DefaultDictionaryTransformer,
)
from ptext.io.transform.object.default_stream_transformer import (
    DefaultStreamTransformer,
)
from ptext.io.transform.page.default_page_dictionary_transformer import (
    DefaultPageDictionaryTransformer,
)
from ptext.io.transform.primitive.default_number_transformer import (
    DefaultNumberTransformer,
)
from ptext.io.transform.primitive.default_string_transformer import (
    DefaultStringTransformer,
)
from ptext.io.transform.reference.default_indirect_object_transformer import (
    DefaultIndirectObjectTransformer,
)
from ptext.io.transform.reference.default_reference_transformer import (
    DefaultReferenceTransformer,
)
from ptext.io.transform.reference.default_xref_transformer import DefaultXREFTransformer
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultLowLevelObjectTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.add_child_transformer(DefaultXREFTransformer())
        # fonts
        self.add_child_transformer(DefaultFontDictionaryTransformer())
        self.add_child_transformer(DefaultFontDescriptorDictionaryTransformer())
        # images
        self.add_child_transformer(DefaultCCITTFaxImageTransformer())
        self.add_child_transformer(DefaultDCTDecodeImageTransformer())
        self.add_child_transformer(DefaultGrayscaleImageTransformer())
        self.add_child_transformer(DefaultJBIG2ImageTransformer())
        self.add_child_transformer(DefaultJPEG2000ImageTransformer())
        self.add_child_transformer(DefaultJPEGImageTransformer())
        # pages
        self.add_child_transformer(DefaultPageDictionaryTransformer())
        # references
        self.add_child_transformer(DefaultIndirectObjectTransformer())
        self.add_child_transformer(DefaultReferenceTransformer())
        # primitives
        self.add_child_transformer(DefaultStreamTransformer())
        self.add_child_transformer(DefaultStringTransformer())
        self.add_child_transformer(DefaultNumberTransformer())
        # objects
        self.add_child_transformer(DefaultDictionaryTransformer())
        self.add_child_transformer(DefaultArrayTransformer())

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
