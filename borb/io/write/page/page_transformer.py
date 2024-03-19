#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible
for writing Dictionary objects of /Type /Page
"""
import logging
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.io.write.font.subsetter import Subsetter
from borb.io.write.object.dictionary_transformer import DictionaryTransformer
from borb.io.write.transformer import WriteTransformerState
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page

logger = logging.getLogger(__name__)


class PageTransformer(DictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible
    for writing Dictionary objects of /Type /Page
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is a /Page Dictionary
        :param object:  the object to be transformed
        :return:        True if the object is a /Page Dictionary, False otherwise
        """
        return (
            isinstance(object, Dictionary)
            and "Type" in object
            and object["Type"] == "Page"
        )

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a /Page Dictionary into a byte stream
        :param object_to_transform:     the /Page Dictionary to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) /Page Dictionary
        """
        # fmt: off
        assert isinstance(object_to_transform, Dictionary)
        assert isinstance(object_to_transform, Page)
        assert (context is not None), "context must be defined in order to write Page objects."
        assert context.root_object is not None, "context.root_object must be defined in order to write Page objects."
        assert isinstance(context.root_object, Document), "context.root_object must be of type Document in order to write Page objects."
        # fmt: on

        pages_dict = context.root_object["XRef"]["Trailer"]["Root"]["Pages"]

        # add /Parent reference to /Pages
        object_to_transform[Name("Parent")] = self.get_reference(pages_dict, context)

        # mark some keys as non-referencable
        for k in ["ArtBox", "BleedBox", "CropBox", "MediaBox", "TrimBox"]:
            if k in object_to_transform:
                object_to_transform[k].set_is_inline(True)

        # apply subsetting
        if context.apply_font_subsetting:
            page = Subsetter.apply(object_to_transform)

        # delegate to super
        super(PageTransformer, self).transform(object_to_transform, context)
