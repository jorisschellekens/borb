#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer acts as an aggregator for
its child transformers, allowing it to transform AnyPDFType
"""
import io
from typing import Optional, Union

from borb.io.read.types import AnyPDFType
from borb.io.write.ascii_art.write_ascii_art_transformer import (
    WriteASCIIArtTransformer,
)
from borb.io.write.image.write_image_transformer import WriteImageTransformer
from borb.io.write.object.write_array_transformer import WriteArrayTransformer
from borb.io.write.object.write_dictionary_transformer import (
    WriteDictionaryTransformer,
)
from borb.io.write.object.write_stream_transformer import WriteStreamTransformer
from borb.io.write.page.write_page_transformer import WritePageTransformer
from borb.io.write.page.write_pages_transformer import WritePagesTransformer
from borb.io.write.primitive.write_boolean_transformer import WriteBooleanTransformer
from borb.io.write.primitive.write_name_transformer import WriteNameTransformer
from borb.io.write.primitive.write_number_transformer import WriteNumberTransformer
from borb.io.write.primitive.write_string_transformer import WriteStringTransformer
from borb.io.write.reference.write_reference_transformer import WriteReferenceTransform
from borb.io.write.reference.write_xref_transformer import WriteXREFTransformer
from borb.io.write.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)
from borb.io.write.write_pdf_transformer import WritePDFTransformer
from borb.io.write.xmp.write_xmp_transformer import WriteXMPTransformer


class WriteAnyObjectTransformer(WriteBaseTransformer):
    """
    This implementation of WriteBaseTransformer acts as an aggregator for
    its child transformers, allowing it to transform AnyPDFType
    """

    def __init__(self):
        super().__init__()
        # fun
        self.add_child_transformer(WriteASCIIArtTransformer())
        # special object types
        self.add_child_transformer(WritePDFTransformer())
        self.add_child_transformer(WriteXREFTransformer())
        self.add_child_transformer(WritePagesTransformer())
        self.add_child_transformer(WritePageTransformer())
        # object types
        self.add_child_transformer(WriteArrayTransformer())
        self.add_child_transformer(WriteStreamTransformer())
        self.add_child_transformer(WriteDictionaryTransformer())
        self.add_child_transformer(WriteImageTransformer())
        self.add_child_transformer(WriteXMPTransformer())
        # primitives
        self.add_child_transformer(WriteNameTransformer())
        self.add_child_transformer(WriteStringTransformer())
        self.add_child_transformer(WriteReferenceTransform())
        self.add_child_transformer(WriteNumberTransformer())
        self.add_child_transformer(WriteBooleanTransformer())

    def can_be_transformed(self, object_to_transform: AnyPDFType):
        """
        This function returns True if the object to be transformed
        can be transformed by this WriteBaseTransformer
        """
        return False

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
        destination: Optional[Union[io.BufferedIOBase, io.RawIOBase]] = None,
    ):
        """
        This method writes an (PDF) object to a byte stream
        """
        if context is None:
            super().transform(
                object_to_transform,
                WriteTransformerContext(
                    destination=destination, root_object=object_to_transform
                ),
            )
        else:
            super().transform(object_to_transform, context)
