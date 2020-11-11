import io
from typing import Optional, Union, List

from ptext.object.pdf_high_level_object import PDFHighLevelObject, EventListener
from ptext.primitive.pdf_object import PDFObject
from ptext.tranform.base_transformer import BaseTransformer, TransformerContext
from ptext.tranform.default_array_transformer import DefaultArrayTransformer
from ptext.tranform.default_dictionary_transformer import DefaultDictionaryTransformer
from ptext.tranform.default_indirect_object_transformer import (
    DefaultIndirectObjectTransformer,
)
from ptext.tranform.default_name_transformer import DefaultNameTransformer
from ptext.tranform.default_number_transformer import DefaultNumberTransformer
from ptext.tranform.default_page_dictionary_transformer import (
    DefaultPageDictionaryTransformer,
)
from ptext.tranform.default_reference_transformer import DefaultReferenceTransformer
from ptext.tranform.default_stream_transformer import DefaultStreamTransformer
from ptext.tranform.default_string_transformer import DefaultStringTransformer
from ptext.tranform.default_xref_transformer import DefaultXREFTransformer
from ptext.tranform.font.default_font_descriptor_dictionary_transformer import (
    DefaultFontDescriptorDictionaryTransformer,
)
from ptext.tranform.font.default_font_dictionary_transformer import (
    DefaultFontDictionaryTransformer,
)
from ptext.tranform.image.default_ccitt_fax_image_transformer import (
    DefaultCCITTFaxImageTransformer,
)
from ptext.tranform.image.default_jbig2_image_transformer import (
    DefaultJBIG2ImageTransformer,
)
from ptext.tranform.image.default_jpeg_2000_image_transformer import (
    DefaultJPEG2000ImageTransformer,
)
from ptext.tranform.image.default_jpeg_image_transformer import (
    DefaultJPEGImageTransformer,
)


class DefaultLowLevelObjectTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.add_child_transformer(DefaultXREFTransformer())
        # fonts
        self.add_child_transformer(DefaultFontDictionaryTransformer())
        self.add_child_transformer(DefaultFontDescriptorDictionaryTransformer())
        # images
        self.add_child_transformer(DefaultJPEGImageTransformer())
        self.add_child_transformer(DefaultJPEG2000ImageTransformer())
        self.add_child_transformer(DefaultJBIG2ImageTransformer())
        self.add_child_transformer(DefaultCCITTFaxImageTransformer())
        # pages
        self.add_child_transformer(DefaultPageDictionaryTransformer())
        # objects
        self.add_child_transformer(DefaultDictionaryTransformer())
        self.add_child_transformer(DefaultArrayTransformer())
        # references
        self.add_child_transformer(DefaultIndirectObjectTransformer())
        self.add_child_transformer(DefaultReferenceTransformer())
        # primitives
        self.add_child_transformer(DefaultStreamTransformer())
        self.add_child_transformer(DefaultNameTransformer())
        self.add_child_transformer(DefaultStringTransformer())
        self.add_child_transformer(DefaultNumberTransformer())

    def can_be_transformed(self, object: Union[io.IOBase, PDFObject]) -> bool:
        return isinstance(object, io.IOBase)

    def transform(
        self,
        object_to_transform: PDFObject,
        parent_object: PDFObject,
        context: Optional[TransformerContext] = None,
        event_listeners: List[EventListener] = [],
    ) -> PDFHighLevelObject:
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
