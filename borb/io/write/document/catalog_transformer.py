#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing /Catalog Dictionary objects
"""
import logging
import zlib
from pathlib import Path
from typing import Optional

from borb.io.read.types import (
    AnyPDFType,
    Dictionary,
    Name,
    String,
    List as bList,
    Stream,
    Decimal as bDecimal,
)
from borb.io.write.object.dictionary_transformer import DictionaryTransformer
from borb.io.write.transformer import WriteTransformerState
from borb.pdf.document.document import Document

logger = logging.getLogger(__name__)


class CatalogTransformer(DictionaryTransformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing /Catalog Dictionary objects
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _build_rgb_outputintent_dictionary(self, root_dictionary: Dictionary) -> None:

        # TODO check if exists already

        # read color profile bytes
        color_profile_bytes: bytes = b""
        with open(Path(__file__).parent / "resources/sRGB_CS_profile.icm", "rb") as fh:
            color_profile_bytes = fh.read()

        # create dest_output_profile
        dest_output_profile: Stream = Stream()
        dest_output_profile[Name("Alternate")] = Name("DeviceRGB")
        dest_output_profile[Name("DecodedBytes")] = color_profile_bytes
        dest_output_profile[Name("Bytes")] = zlib.compress(color_profile_bytes, 9)
        dest_output_profile[Name("Filter")] = Name("FlateDecode")
        dest_output_profile[Name("Length")] = bDecimal(len(color_profile_bytes))
        dest_output_profile[Name("N")] = bDecimal(3)

        # create RGB OutputIntent
        rgb_outputintent: Dictionary = Dictionary()
        rgb_outputintent[Name("Type")] = Name("OutputIntent")
        rgb_outputintent[Name("S")] = Name("GTS_PDFA1")
        rgb_outputintent[Name("OutputCondition")] = String("")
        rgb_outputintent[Name("OutputConditionIdentifier")] = String("Custom")
        rgb_outputintent[Name("Info")] = String("sRGB IEC61966-2.1")
        rgb_outputintent[Name("RegistryName")] = String("http://www.color.org")
        rgb_outputintent[Name("DestOutputProfile")] = dest_output_profile
        dest_output_profile.set_parent(rgb_outputintent)

        # creatte OutputIntents
        outputintents_array = bList()
        outputintents_array.append(rgb_outputintent)
        rgb_outputintent.set_parent(outputintents_array)

        # add to root_dictionary
        root_dictionary[Name("OutputIntents")] = outputintents_array
        outputintents_array.set_parent(root_dictionary)

    #
    # PUBLIC
    #

    def can_be_transformed(self, any: AnyPDFType):
        """
        This function returns True if the object to be transformed is a /Catalog Dictionary
        """
        return (
            isinstance(any, Dictionary) and "Type" in any and any["Type"] == "Catalog"
        )

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerState] = None,
    ):
        """
        This method writes a /Catalog Dictionary to a byte stream
        """

        assert isinstance(object_to_transform, Dictionary)

        # /OutputIntents
        # fmt: off
        needs_outputintents: bool = (context is not None
                                     and isinstance(context.root_object, Document)
                                     and context.root_object.get_document_info().get_conformance_level_upon_create() is not None)
        if needs_outputintents:
            self._build_rgb_outputintent_dictionary(object_to_transform)
        # fmt: on

        # call super
        return super(CatalogTransformer, self).transform(object_to_transform, context)
