#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of \Type \Page
"""
import logging
import typing
from typing import Optional

from ptext.io.read.types import (
    AnyPDFType,
    Dictionary,
    Name,
)
from ptext.io.write.object.write_dictionary_transformer import (
    WriteDictionaryTransformer,
)
from ptext.io.write.write_base_transformer import (
    WriteTransformerContext,
)
from ptext.pdf.document import Document

logger = logging.getLogger(__name__)


class WritePageTransformer(WriteDictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of \Type \Page
    """

    def __init__(self):
        self.queue: typing.List[AnyPDFType] = []

    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Dictionary) and "Type" in any and any["Type"] == "Page"

    def _is_pages_dictionary(self, object):
        if object is None:
            return False
        if not isinstance(object, Dictionary):
            return False
        if "Type" in object and object["Type"] == "Pages":
            return True
        if "Count" in object and "Kids" in object:
            return True
        return False

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert isinstance(object_to_transform, Dictionary)
        assert context is not None
        assert context.root_object is not None

        assert isinstance(context.root_object, Document)
        pages_dict = context.root_object["XRef"]["Trailer"]["Root"]["Pages"]

        # add \Parent reference to \Pages
        object_to_transform[Name("Parent")] = self.get_reference(pages_dict, context)

        # delegate to super
        super(WritePageTransformer, self).transform(object_to_transform, context)
