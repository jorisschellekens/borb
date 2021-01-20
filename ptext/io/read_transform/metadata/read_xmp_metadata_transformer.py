import io
import typing
import xml
from typing import Optional, Any, Union

from ptext.io.read_transform.object.read_stream_transformer import ReadStreamTransformer
from ptext.io.read_transform.read_base_transformer import (
    ReadTransformerContext,
)
from ptext.io.read_transform.types import (
    AnyPDFType,
    Stream,
)
from ptext.pdf.canvas.event.event_listener import EventListener


class ReadXMPMetadataTransformer(ReadStreamTransformer):
    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Stream)
            and "Type" in object
            and object["Type"] == "Metadata"
            and "Subtype" in object
            and object["Subtype"] == "XML"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # delegate to super
        out_value = super(ReadXMPMetadataTransformer, self).transform(
            object_to_transform=object_to_transform,
            parent_object=parent_object,
            context=context,
            event_listeners=event_listeners,
        )

        # parse XML
        assert out_value is not None
        assert isinstance(out_value, Stream)
        assert "DecodedBytes" in out_value
        try:
            xml_root = xml.etree.ElementTree.fromstring(
                out_value["DecodedBytes"].decode("latin1")
            )
        except:
            pass
        # TODO
        # A metadata stream may be attached to a document through the Metadata entry in the document catalogue
        # (see 7.7.2, “Document Catalog”). The metadata framework provides a date stamp for metadata expressed in
        # the framework. If this date stamp is equal to or later than the document modification date recorded in the
        # document information dictionary, the metadata stream shall be taken as authoritative. If, however, the
        # document modification date recorded in the document information dictionary is later than the metadata
        # stream’s date stamp, the document has likely been saved by a writer that is not aware of metadata streams. In
        # this case, information stored in the document information dictionary shall be taken to override any semantically
        # equivalent items in the metadata stream. In addition, PDF document components represented as a stream or
        # dictionary may have a Metadata entry (see Table 316).
