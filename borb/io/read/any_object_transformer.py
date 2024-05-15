#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer aggregates all
other implementations of ReadBaseTransformer
"""
import io
import typing

# fmt: off
from borb.io.read.font.font_dictionary_transformer import FontDictionaryTransformer
from borb.io.read.function.function_dictionary_transformer import FunctionDictionaryTransformer
from borb.io.read.image.ccitt_fax_image_transformer import CCITTFaxImageTransformer
from borb.io.read.image.compressed_jpeg_image_transformer import CompressedJPEGImageTransformer
from borb.io.read.image.grayscale_image_transformer import GrayscaleImageTransformer
from borb.io.read.image.jbig2_image_transformer import JBIG2ImageTransformer
from borb.io.read.image.jpeg_2000_image_transformer import JPEG2000ImageTransformer
from borb.io.read.image.jpeg_image_transformer import JPEGImageTransformer
from borb.io.read.metadata.xmp_metadata_transformer import XMPMetadataTransformer
from borb.io.read.object.array_transformer import ArrayTransformer
from borb.io.read.object.dictionary_transformer import DictionaryTransformer
from borb.io.read.object.stream_transformer import StreamTransformer
from borb.io.read.page.page_dictionary_transformer import PageDictionaryTransformer
from borb.io.read.page.root_dictionary_transformer import RootDictionaryTransformer
from borb.io.read.primitive.number_transformer import NumberTransformer
from borb.io.read.primitive.string_transformer import StringTransformer
from borb.io.read.reference.reference_transformer import ReferenceTransformer
from borb.io.read.reference.xref_transformer import XREFTransformer
from borb.io.read.transformer import ReadTransformerState
from borb.io.read.transformer import Transformer
from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.event.event_listener import EventListener


# fmt: on


class AnyObjectTransformer(Transformer):
    """
    This implementation of ReadBaseTransformer aggregates all other implementations
    of ReadBaseTransformer
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__()
        self.add_child_transformer(XREFTransformer())
        # XMP
        self.add_child_transformer(XMPMetadataTransformer())
        # fonts
        self.add_child_transformer(FontDictionaryTransformer())
        # images
        self.add_child_transformer(CCITTFaxImageTransformer())
        self.add_child_transformer(GrayscaleImageTransformer())
        self.add_child_transformer(JBIG2ImageTransformer())
        self.add_child_transformer(JPEG2000ImageTransformer())
        self.add_child_transformer(JPEGImageTransformer())
        self.add_child_transformer(CompressedJPEGImageTransformer())
        # pages
        self.add_child_transformer(RootDictionaryTransformer())
        self.add_child_transformer(PageDictionaryTransformer())
        # references
        self.add_child_transformer(ReferenceTransformer())
        # primitives
        self.add_child_transformer(FunctionDictionaryTransformer())
        self.add_child_transformer(StreamTransformer())
        self.add_child_transformer(StringTransformer())
        self.add_child_transformer(NumberTransformer())
        # objects
        self.add_child_transformer(DictionaryTransformer())
        self.add_child_transformer(ArrayTransformer())

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(
        self,
        object: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType],
    ) -> bool:
        """
        This function returns True if the object to be transformed can be transformed by this ReadAnyObjectTransformer
        """
        return isinstance(object, io.IOBase)

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function reads an object from a byte stream.
        The object being read depends on the implementation of ReadAnyObjectTransformer.
        """
        if context is None:
            return super().transform(
                object_to_transform,
                parent_object,
                ReadTransformerState(),
                event_listeners,
            )
        else:
            return super().transform(
                object_to_transform, parent_object, context, event_listeners
            )
