#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer
is responsible for writing XMP meta-data information
"""
import logging
import typing
import xml.etree.ElementTree

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState

logger = logging.getLogger(__name__)


class XMPTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing XMP meta-data information
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
        This function returns True if the object to be transformed is an xml.etree.ElementTree.Element
        :param object:  the object to be transformed
        :return:        True if the object is an xml.etree.ElementTree.Element, False otherwise
        """
        return isinstance(object, xml.etree.ElementTree.Element)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms an xml.etree.ElementTree.Element Object into a byte stream
        :param object_to_transform:     the xml.etree.ElementTree.Element Object to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) xml.etree.ElementTree.Element Object
        """
        assert isinstance(object_to_transform, xml.etree.ElementTree.Element)
        # fmt: off
        assert context is not None, "A WriteTransformerState must be defined in order to write XMP objects."
        assert context.destination is not None, "A WriteTransformerState must be defined in order to write XMP objects."
        # fmt: on

        # build stream
        out_value = Stream()
        out_value[Name("Type")] = Name("Metadata")
        out_value[Name("Subtype")] = Name("XML")

        bts = xml.etree.ElementTree.tostring(object_to_transform)
        out_value[Name("DecodedBytes")] = bts
        out_value[Name("Bytes")] = bts
        out_value[Name("Length")] = bDecimal(len(bts))

        # copy reference
        out_value.set_reference(object_to_transform.get_reference())  # type: ignore[attr-defined]

        # start object if needed
        started_object = False
        ref = out_value.get_reference()
        if ref is not None:
            assert isinstance(ref, Reference)
            if ref.object_number is not None and ref.byte_offset is None:
                started_object = True
                self._start_object(out_value, context)

        # pass stream along to other transformer
        self.get_root_transformer().transform(out_value, context)

        # end object if needed
        if started_object:
            self._end_object(out_value, context)
