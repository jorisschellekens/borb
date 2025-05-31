#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor class that injects XMP metadata into a PDF document.

This class extends `WriteNewVisitor` and is responsible for adding XMP metadata
to PDF documents. It follows the visitor design pattern and can be used to
traverse a PDF document's nodes and inject metadata based on the document's
conformance level. The metadata is injected only once per session to avoid
redundant changes.

The XMP metadata injection includes information such as the document's
producer, keywords, creation date, author, title, and more, with the format
conforming to Adobe's XMP specification. The class also ensures that the
metadata injection complies with the document's conformance level (e.g., PDF/A).
"""
import typing

from borb.pdf.conformance import Conformance
from borb.pdf.primitives import stream, name
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class InjectXMPMetadataVisitor(WriteNewVisitor):
    """
    A visitor class that injects XMP metadata into a PDF document.

    This class extends `WriteNewVisitor` and is responsible for adding XMP metadata
    to PDF documents. It follows the visitor design pattern and can be used to
    traverse a PDF document's nodes and inject metadata based on the document's
    conformance level. The metadata is injected only once per session to avoid
    redundant changes.

    The XMP metadata injection includes information such as the document's
    producer, keywords, creation date, author, title, and more, with the format
    conforming to Adobe's XMP specification. The class also ensures that the
    metadata injection complies with the document's conformance level (e.g., PDF/A).
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __get_xmp_date_format_from_iso_8824_date_format(s: str) -> str:
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
    def __get_xmp_stream_bytes(
        conformance: typing.Optional[Conformance],
        info_dictionary: typing.Dict[str, typing.Any],
    ) -> bytes:

        # start packet
        s: str = '<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>'
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
            d["xmp:CreateDate"] = InjectXMPMetadataVisitor.__get_xmp_date_format_from_iso_8824_date_format(info_dictionary["CreationDate"])
            # fmt: on
        if "Creator" in info_dictionary:
            d["xmp:CreatorTool"] = str(info_dictionary["Creator"])
        if "ModDate" in info_dictionary:
            # fmt: off
            d["xmp:ModifyDate"] = InjectXMPMetadataVisitor.__get_xmp_date_format_from_iso_8824_date_format(info_dictionary["ModDate"])
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
        # fmt: off
        if conformance is not None:
            s += '\n\t\t<rdf:Description rdf:about="" xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/">'
            s += "\n\t\t\t<pdfaid:part>%d</pdfaid:part>" % conformance.get_version()
            s += "\n\t\t\t<pdfaid:conformance>%s</pdfaid:conformance>" % conformance.get_level()
            s += "\n\t\t</rdf:Description>"
        # fmt: on

        # close package
        s += "\n\t</rdf:RDF>"
        s += "\n</x:xmpmeta>"
        s += '\n<?xpacket end="w"?>'

        # return
        return s.encode("latin1")

    #
    # PUBLIC
    #

    def visit(self, node: typing.Any) -> typing.Optional[typing.Any]:
        """
        Traverse the PDF document tree using the visitor pattern.

        This method is called when a node does not have a specialized handler.
        Subclasses can override this method to provide default behavior or logging
        for unsupported nodes. If any operation is performed on the node (e.g.,
        writing or persisting), the method returns `True`. Otherwise, it returns
        `False` to indicate that the visitor did not process the node.

        :param node:    the node (PDFType) to be processed
        :return:        True if the visitor processed the node False otherwise
        """
        # check whether this is a document
        from borb.pdf.document import Document

        if not isinstance(node, Document):
            return False
        conformance: typing.Optional[Conformance] = node.get_conformance_at_create()
        if conformance is None:
            return False
        if not conformance.requires_xmp_metadata():
            return False
        if "Trailer" not in node:
            return False
        if "Root" not in node["Trailer"]:
            return False
        if "Info" not in node["Trailer"]:
            return False

        # get Catalog
        catalog: typing.Dict[typing.Union[name, str], typing.Any] = node["Trailer"][
            "Root"
        ]

        # IF the PDF already has XMP metadata
        # THEN do not attempt to inject XMP metadata
        if catalog.get("Metadata", {}).get("Subtype", None) == "XML":
            return False

        # IF the document conformance level demands XMP metadata
        # THEN add XMP metadata
        info_dictionary: dict = node["Trailer"]["Info"]
        xmp_metadata_stream: stream = stream(
            {
                name("Type"): name("Metadata"),
                name("Subtype"): name("XML"),
                name("Bytes"): InjectXMPMetadataVisitor.__get_xmp_stream_bytes(
                    conformance=node.get_conformance_at_create(),
                    info_dictionary=info_dictionary,
                ),
            }
        )
        xmp_metadata_stream[name("Length")] = len(xmp_metadata_stream["Bytes"])
        xmp_metadata_stream.pop("Filter")
        catalog[name("Metadata")] = xmp_metadata_stream

        # call other visitor(s)
        super().go_to_root_and_visit(node=node)

        # return
        return True
