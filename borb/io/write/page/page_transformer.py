#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible
for writing Dictionary objects of \Type \Page
"""
import logging
from typing import Optional

from borb.io.read.types import AnyPDFType, Dictionary, Name
from borb.io.write.object.dictionary_transformer import DictionaryTransformer
from borb.io.write.transformer import WriteTransformerState
from borb.pdf.document import Document

logger = logging.getLogger(__name__)


class PageTransformer(DictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of \Type \Page
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents an \Page Dictionary
        """
        return isinstance(any, Dictionary) and "Type" in any and any["Type"] == "Page"

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes a \Page Dictionary to a byte stream
        """
        assert isinstance(object_to_transform, Dictionary)
        assert (
            context is not None
        ), "A WriteTransformerState must be defined in order to write Page objects."
        assert context.root_object is not None

        assert isinstance(context.root_object, Document)
        pages_dict = context.root_object["XRef"]["Trailer"]["Root"]["Pages"]

        # add \Parent reference to \Pages
        object_to_transform[Name("Parent")] = self.get_reference(pages_dict, context)

        # mark some keys as non-referencable
        for k in ["ArtBox", "BleedBox", "CropBox", "MediaBox", "TrimBox"]:
            if k in object_to_transform:
                object_to_transform[k].set_can_be_referenced(False)  # type: ignore [attr-defined]

        # delegate to super
        super(PageTransformer, self).transform(object_to_transform, context)
