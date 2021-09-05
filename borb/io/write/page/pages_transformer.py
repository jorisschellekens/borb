#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible
for writing Dictionary objects of \Type \Pages
"""
import logging
import typing
from typing import Optional

from borb.io.read.types import AnyPDFType, Dictionary, Name, Reference
from borb.io.write.object.dictionary_transformer import DictionaryTransformer
from borb.io.write.transformer import WriteTransformerState

logger = logging.getLogger(__name__)


class PagesTransformer(DictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of \Type \Pages
    """

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be converted represents a \Pages Dictionary
        """
        return isinstance(any, Dictionary) and "Type" in any and any["Type"] == "Pages"

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes a \Pages Dictionary to a byte stream
        """
        assert isinstance(object_to_transform, Dictionary)
        assert (
            context is not None
        ), "A WriteTransformerState must be defined in order to write Pages Dictionary objects."

        # \Kids can be written immediately
        object_to_transform[Name("Kids")].set_can_be_referenced(False)  # type: ignore [attr-defined]

        # queue writing of \Page objects
        queue: typing.List[AnyPDFType] = []
        for i, k in enumerate(object_to_transform["Kids"]):
            queue.append(k)
            ref: Reference = self.get_reference(k, context)
            object_to_transform["Kids"][i] = ref

        # delegate to super
        super(PagesTransformer, self).transform(object_to_transform, context)

        # write \Page objects
        for p in queue:
            self.get_root_transformer().transform(p, context)

        # restore \Kids
        for i, k in enumerate(queue):
            object_to_transform["Kids"][i] = k
