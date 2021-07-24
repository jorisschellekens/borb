# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer aggregates all
other implementations of ReadBaseTransformer
"""
import io
import typing
from typing import Any, Optional, Union

from borb.io.read.font.read_font_dictionary_transformer import (
    ReadFontDictionaryTransformer,
)
from borb.io.read.function.read_function_dictionary_transformer import (
    FunctionDictionaryTransformer,
)
from borb.io.read.image.read_ccitt_fax_image_transformer import (
    ReadCCITTFaxImageTransformer,
)
from borb.io.read.image.read_compressed_jpeg_image_transformer import (
    ReadCompressedJPEGImageTransformer,
)
from borb.io.read.image.read_grayscale_image_transformer import (
    ReadGrayscaleImageTransformer,
)
from borb.io.read.image.read_jbig2_image_transformer import ReadJBIG2ImageTransformer
from borb.io.read.image.read_jpeg_2000_image_transformer import (
    ReadJPEG2000ImageTransformer,
)
from borb.io.read.image.read_jpeg_image_transformer import ReadJPEGImageTransformer
from borb.io.read.metadata.read_xmp_metadata_transformer import (
    ReadXMPMetadataTransformer,
)
from borb.io.read.object.read_array_transformer import ReadArrayTransformer
from borb.io.read.object.read_dictionary_transformer import ReadDictionaryTransformer
from borb.io.read.object.read_stream_transformer import ReadStreamTransformer
from borb.io.read.page.read_page_dictionary_transformer import (
    ReadPageDictionaryTransformer,
)
from borb.io.read.page.read_root_dictionary_transformer import (
    ReadRootDictionaryTransformer,
)
from borb.io.read.primitive.read_number_transformer import ReadNumberTransformer
from borb.io.read.primitive.read_string_transformer import ReadStringTransformer
from borb.io.read.read_base_transformer import (
    ReadBaseTransformer,
    ReadTransformerContext,
)
from borb.io.read.reference.read_reference_transformer import ReadReferenceTransformer
from borb.io.read.reference.read_xref_transformer import ReadXREFTransformer
from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.event.event_listener import EventListener


class ReadAnyObjectTransformer(ReadBaseTransformer):
    """
    This implementation of ReadBaseTransformer aggregates all other implementations
    of ReadBaseTransformer
    """

    def __init__(self):
        super().__init__()
        self.add_child_transformer(ReadXREFTransformer())
        # XMP
        self.add_child_transformer(ReadXMPMetadataTransformer())
        # fonts
        self.add_child_transformer(ReadFontDictionaryTransformer())
        # images
        self.add_child_transformer(ReadCCITTFaxImageTransformer())
        self.add_child_transformer(ReadGrayscaleImageTransformer())
        self.add_child_transformer(ReadJBIG2ImageTransformer())
        self.add_child_transformer(ReadJPEG2000ImageTransformer())
        self.add_child_transformer(ReadJPEGImageTransformer())
        self.add_child_transformer(ReadCompressedJPEGImageTransformer())
        # pages
        self.add_child_transformer(ReadRootDictionaryTransformer())
        self.add_child_transformer(ReadPageDictionaryTransformer())
        # references
        self.add_child_transformer(ReadReferenceTransformer())
        # primitives
        self.add_child_transformer(FunctionDictionaryTransformer())
        self.add_child_transformer(ReadStreamTransformer())
        self.add_child_transformer(ReadStringTransformer())
        self.add_child_transformer(ReadNumberTransformer())
        # objects
        self.add_child_transformer(ReadDictionaryTransformer())
        self.add_child_transformer(ReadArrayTransformer())

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed can be transformed by this ReadAnyObjectTransformer
        """
        return isinstance(object, io.IOBase)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads an object from a byte stream.
        The object being read depends on the implementation of ReadAnyObjectTransformer.
        """
        if context is None:
            return super().transform(
                object_to_transform,
                parent_object,
                ReadTransformerContext(),
                event_listeners,
            )
        else:
            return super().transform(
                object_to_transform, parent_object, context, event_listeners
            )
