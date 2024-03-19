#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing /Info Dictionary objects
"""
import datetime
import logging
import random
import typing
import xml.etree.ElementTree

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.io.read.types import Stream
from borb.io.read.types import String
from borb.io.write.conformance_level import ConformanceLevel
from borb.io.write.object.dictionary_transformer import DictionaryTransformer
from borb.io.write.object.stream_transformer import StreamTransformer
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState
from borb.license.version import Version
from borb.pdf.document.document import Document
from borb.pdf.trailer.document_info import XMPDocumentInfo

logger = logging.getLogger(__name__)


class InformationDictionaryTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing /Info Dictionary objects
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _consolidate_xmp_and_info_dictionary(self, document: Document) -> Dictionary:
        new_info_dictionary: Dictionary = Dictionary()

        # get /Info Dictionary
        if (
            "XRef" in document
            and "Trailer" in document["XRef"]
            and "Info" in document["XRef"]["Trailer"]
            and isinstance(document["XRef"]["Trailer"]["Info"], Dictionary)
        ):
            info_dictionary: Dictionary = document["XRef"]["Trailer"]["Info"]
            for k, v in info_dictionary.items():
                new_info_dictionary[k] = v

        # get XMP /Metadata
        if (
            "XRef" in document
            and "Trailer" in document["XRef"]
            and "Root" in document["XRef"]["Trailer"]
            and "Metadata" in document["XRef"]["Trailer"]["Root"]
            and isinstance(
                document["XRef"]["Trailer"]["Root"]["Metadata"],
                xml.etree.ElementTree.Element,
            )
        ):
            xmp_document_info: XMPDocumentInfo = document.get_xmp_document_info()
            for k, v in {
                Name("Title"): xmp_document_info.get_title(),
                Name("Author"): xmp_document_info.get_author(),
                Name("Subject"): xmp_document_info.get_subject(),
                Name("Keywords"): xmp_document_info.get_keywords(),
                Name("Creator"): xmp_document_info.get_creator(),
                Name("Producer"): xmp_document_info.get_producer(),
                Name("CreationDate"): xmp_document_info.get_creation_date(),
                Name("ModDate"): xmp_document_info.get_modification_date(),
            }.items():
                if v is None:
                    continue
                if k in ["CreationDate", "ModDate"]:
                    v = InformationDictionaryTransformer._convert_xmp_date_format_to_iso_8824_date_format(
                        v
                    )
                new_info_dictionary[k] = String(v)

        # return
        return new_info_dictionary

    @staticmethod
    def _convert_iso_8824_date_format_to_xmp_date_format(s: str) -> str:
        try:
            year: str = s[2:6]
            month: str = s[6:8]
            day: str = s[8:10]
            hour: str = s[10:12]
            minute: str = s[12:14]
            second: str = s[14:16]
            # fmt: off
            return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "+00:00"
            # fmt: on
        except:
            return s

    @staticmethod
    def _convert_xmp_date_format_to_iso_8824_date_format(s: str) -> str:
        return s

    @staticmethod
    def _now_as_iso_8824_date_format() -> str:
        timestamp_str = "D:"
        now = datetime.datetime.now()
        for n in [now.year, now.month, now.day, now.hour, now.minute, now.second]:
            timestamp_str += "{0:02}".format(n)
        timestamp_str += "Z00"
        return timestamp_str

    def _update_info_dictionary(self, info_dictionary: Dictionary) -> Dictionary:
        # set CreationDate
        # fmt: off
        if "CreationDate" not in info_dictionary:
            info_dictionary[Name("CreationDate")] = String(InformationDictionaryTransformer._now_as_iso_8824_date_format())
        # fmt: on

        # set ModDate
        # fmt: off
        info_dictionary[Name("ModDate")] = String(InformationDictionaryTransformer._now_as_iso_8824_date_format())
        # fmt: on

        # set Producer
        # fmt: off
        info_dictionary[Name("Producer")] = String(Version.get_producer() + " " + Version.get_version())
        # fmt: on

        # return
        return info_dictionary

    def _write_xmp_metadata_stream(
        self,
        info_dictionary: Dictionary,
        conformance_level: typing.Optional[ConformanceLevel] = None,
    ) -> Stream:
        random_id: str = "".join(
            [
                random.choice("0123456789abcdefghijklmnopqrstuvwxyz")
                for _ in range(0, 24)
            ]
        )
        s: str = '<?xpacket begin="" id="%s"?>' % random_id
        s += '\n<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.1.0-jc003">'
        s += '\n\t<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'

        # rdf:Description
        d: typing.Dict[str, str] = {
            "rdf:about": "",
            "xmlns:dc": "http://purl.org/dc/elements/1.1/",
            "xmlns:pdf": "http://ns.adobe.com/pdf/1.3/",
            "xmlns:xmp": "http://ns.adobe.com/xap/1.0/",
            "dc:format": "application/pdf",
        }
        if "Producer" in info_dictionary:
            d["pdf:Producer"] = str(info_dictionary["Producer"])
        if "Keywords" in info_dictionary:
            d["pdf:Keywords"] = str(info_dictionary["Keywords"])
        if "CreationDate" in info_dictionary:
            # fmt: off
            d["xmp:CreateDate"] = InformationDictionaryTransformer._convert_iso_8824_date_format_to_xmp_date_format(info_dictionary["CreationDate"])
            # fmt: on
        if "Creator" in info_dictionary:
            d["xmp:CreatorTool"] = str(info_dictionary["Creator"])
        if "ModDate" in info_dictionary:
            # fmt: off
            d["xmp:ModifyDate"] = InformationDictionaryTransformer._convert_iso_8824_date_format_to_xmp_date_format(info_dictionary["ModDate"])
            # fmt: on
        s += (
            "\n\t\t<rdf:Description"
            + "".join([("\n\t\t " + k + '="' + v + '"') for k, v in d.items()])
            + ">"
        )

        # Author
        if "Author" in info_dictionary:
            s += (
                "\n\t\t\t<dc:creator>\n\t\t\t\t<rdf:Seq>\n\t\t\t\t\t<rdf:li>"
                + str(info_dictionary["Author"])
                + "</rdf:li>\n\t\t\t\t</rdf:Seq>\n\t\t\t</dc:creator>"
            )
        # Keywords
        if "Keywords" in info_dictionary:
            s += (
                "\n\t\t\t<dc:subject>\n\t\t\t\t<rdf:Bag>"
                + "".join(
                    [
                        ("\n\t\t\t\t\t<rdf:li>" + x.strip() + "</rdf:li>")
                        for x in str(info_dictionary["Keywords"]).split(" ")
                    ]
                )
                + "\n\t\t\t\t</rdf:Bag>\n\t\t\t</dc:subject>"
            )
        # Subject
        # fmt: off
        if "Subject" in info_dictionary:
            s += '\n\t\t\t<dc:description>\n\t\t\t\t<rdf:Alt>\n\t\t\t\t\t<rdf:li xml:lang="x-default">' + str(info_dictionary["Subject"]) + "</rdf:li>\n\t\t\t\t</rdf:Alt>\n\t\t\t</dc:description>"
        # fmt: on

        # Title
        # fmt: off
        if "Title" in info_dictionary:
            s += '\n\t\t\t<dc:title>\n\t\t\t\t<rdf:Alt>\n\t\t\t\t\t<rdf:li xml:lang="x-default">' + str(info_dictionary["Title"]) + "</rdf:li>\n\t\t\t\t</rdf:Alt>\n\t\t\t</dc:title>"
        # fmt: on

        # close
        s += "\n\t\t</rdf:Description>"

        # version
        if conformance_level is not None:
            s += '\n\t\t<rdf:Description rdf:about="" xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/">'
            s += (
                "\n\t\t\t<pdfaid:part>%d</pdfaid:part>"
                % conformance_level.get_standard()
            )
            s += (
                "\n\t\t\t<pdfaid:conformance>%s</pdfaid:conformance>"
                % conformance_level.get_conformance_level()
            )
            s += "\n\t\t</rdf:Description>"

        # close package
        s += "\n\t</rdf:RDF>"
        s += "\n</x:xmpmeta>"
        s += '\n<?xpacket end="w"?>'

        # build Stream object
        metadata_stream: Stream = Stream()
        metadata_stream[Name("Type")] = Name("Metadata")
        metadata_stream[Name("Subtype")] = Name("XML")
        metadata_stream[Name("Bytes")] = bytes(s, "latin1")
        metadata_stream[Name("Length")] = bDecimal(len(metadata_stream[Name("Bytes")]))

        # return
        return metadata_stream

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is an /Info Dictionary
        :param object:  the object to be transformed
        :return:        True if the object is an /Info Dictionary, False otherwise
        """
        if not isinstance(object, Dictionary):
            return False
        parent: typing.Any = object.get_parent()
        return (
            isinstance(parent, Dictionary)
            and "Info" in parent
            and parent["Info"] == object
        )

    def transform(
        self,
        object_to_transform: typing.Any,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms an /Info Dictionary into a byte stream
        :param object_to_transform:     the /Info Dictionary to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) /Info Dictionary
        """

        # get Document
        document: Document = object_to_transform.get_root()
        assert document is not None
        assert isinstance(document, Document)

        # consolidate XMP /Metadata and /Info Dictionary
        new_info_dictionary: Dictionary = self._consolidate_xmp_and_info_dictionary(
            document
        )

        # update
        self._update_info_dictionary(new_info_dictionary)

        # determine whether XMP /Metadata is needed
        # fmt: off
        has_xmp_metadata: bool = "XRef" in document                                         \
                                   and "Trailer" in document["XRef"]                        \
                                   and "Root" in document["XRef"]["Trailer"]                \
                                   and "Metadata" in document["XRef"]["Trailer"]["Root"]
        needs_xmp_metadata = has_xmp_metadata or (document.get_document_info().get_conformance_level_upon_create() is not None)
        # fmt: on

        if needs_xmp_metadata:
            # write XMP /Metadata
            xmp_metadata_stream: Stream = self._write_xmp_metadata_stream(
                new_info_dictionary,
                document.get_document_info().get_conformance_level_upon_create(),
            )
            assert context is not None
            document["XRef"]["Trailer"]["Root"][Name("Metadata")] = self.get_reference(
                xmp_metadata_stream, context
            )
            xmp_metadata_stream.set_parent(document["XRef"]["Trailer"]["Root"])  # type: ignore[attr-defined]

            # delegate XMP /Metadata
            for h in self.get_root_transformer()._handlers:
                if isinstance(h, StreamTransformer) and h.can_be_transformed(
                    xmp_metadata_stream
                ):
                    h.transform(xmp_metadata_stream, context)
                    break

        # write /Info
        for k, v in new_info_dictionary.items():
            document["XRef"]["Trailer"][Name("Info")][k] = v

        # delegate /Info
        for h in self.get_root_transformer()._handlers:
            if isinstance(h, DictionaryTransformer) and h.can_be_transformed(
                document["XRef"]["Trailer"][Name("Info")]
            ):
                h.transform(document["XRef"]["Trailer"][Name("Info")], context)
                break

        # check reference
        assert document["XRef"]["Trailer"][Name("Info")].get_reference() is not None
        assert (
            document["XRef"]["Trailer"][Name("Info")].get_reference().byte_offset
            is not None
        )
