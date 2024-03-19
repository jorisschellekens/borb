#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A metadata stream may be attached to a document through the Metadata entry in the document catalogue
(see 7.7.2, “Document Catalog”). The metadata framework provides a date stamp for metadata expressed in
the framework. If this date stamp is equal to or later than the document modification date recorded in the
document information dictionary, the metadata stream shall be taken as authoritative. If, however, the
document modification date recorded in the document information dictionary is later than the metadata
stream’s date stamp, the document has likely been saved by a writer that is not aware of metadata streams. In
this case, information stored in the document information dictionary shall be taken to override any semantically
equivalent items in the metadata stream. In addition, PDF document components represented as a stream or
dictionary may have a Metadata entry (see Table 316).
"""
import io
import logging
import typing
import xml.etree.ElementTree

from borb.io.read.object.stream_transformer import StreamTransformer
from borb.io.read.transformer import ReadTransformerState
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Element
from borb.io.read.types import Stream
from borb.pdf.canvas.event.event_listener import EventListener

logger = logging.getLogger(__name__)


class XMPMetadataTransformer(StreamTransformer):
    """
    A metadata stream may be attached to a document through the Metadata entry in the document catalogue
    (see 7.7.2, “Document Catalog”). The metadata framework provides a date stamp for metadata expressed in
    the framework. If this date stamp is equal to or later than the document modification date recorded in the
    document information dictionary, the metadata stream shall be taken as authoritative. If, however, the
    document modification date recorded in the document information dictionary is later than the metadata
    stream’s date stamp, the document has likely been saved by a writer that is not aware of metadata streams. In
    this case, information stored in the document information dictionary shall be taken to override any semantically
    equivalent items in the metadata stream. In addition, PDF document components represented as a stream or
    dictionary may have a Metadata entry (see Table 316).
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

    def can_be_transformed(
        self,
        object: typing.Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType],
    ) -> bool:
        """
        This function returns True if the object to be transformed is a JPEG Image
        :param object:  the object to be transformed
        :return:        True if the object is XML Metadata, False otherwise
        """
        return (
            isinstance(object, Stream)
            and "Type" in object
            and object["Type"] == "Metadata"
            and "Subtype" in object
            and object["Subtype"] == "XML"
        )

    def transform(
        self,
        object_to_transform: typing.Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: typing.Any,
        context: typing.Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> typing.Any:
        """
        This function transforms a Dictionary into an xml.etree.ElementTree Object
        :param object_to_transform:     the Dictionary to transform
        :param parent_object:           the parent Object
        :param context:                 the ReadTransformerState (containing passwords, etc)
        :param event_listeners:         the EventListener objects that may need to be notified
        :return:                        an xml.etree.ElementTree Object
        """

        # delegate to super (ReadStreamTransformer)
        out_value = super(XMPMetadataTransformer, self).transform(
            object_to_transform=object_to_transform,
            parent_object=parent_object,
            context=context,
            event_listeners=event_listeners,
        )

        # parse XML
        assert out_value is not None
        assert isinstance(out_value, Stream)
        assert "DecodedBytes" in out_value
        xml_root_out = None
        try:
            xml_root_orig = xml.etree.ElementTree.fromstring(
                out_value["DecodedBytes"].decode("latin1")
            )

            # make copy so that we can add attributes like parent and listeners
            xml_root_out = Element(xml_root_orig.tag)
            xml_root_out.set_parent(parent_object)
            for e in xml_root_orig:
                xml_root_out.append(e)

        except Exception as ex:
            logger.warning("Unable to process XMP meta-data")

        # return
        return xml_root_out
