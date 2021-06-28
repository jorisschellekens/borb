#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class represents the meta-information belonging to a PDF document
"""
import typing
from decimal import Decimal
from typing import List, Optional


class DocumentInfo:
    """
    This class represents the meta-information belonging to a PDF document
    """

    def __init__(self, document: "Document"):  # type: ignore [name-defined]
        super().__init__()
        self._document: "Document" = document  # type: ignore [name-defined]

    def has_optional_content(self) -> bool:
        """
        Optional content (PDF 1.5) refers to sub-clauses of content in a PDF document that can be selectively viewed
        or hidden by document authors or consumers. This capability is useful in items such as CAD drawings, layered
        artwork, maps, and multi-language documents.
        """
        return "OCProperties" in self._document["XRef"]["Trailer"]

    def get_optional_content_group_names(self) -> typing.List[str]:
        """
        This function returns the name(s) of the optional content group(s),
        suitable for presentation in a reader’s user interface
        """
        if not self.has_optional_content():
            return []
        return [
            str(x["Name"])
            for x in self._document["XRef"]["Trailer"]["OCProperties"]
            if "Name" in x
        ]

    def get_title(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The document’s title.
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["Title"]
        except:
            return None

    def get_creator(self) -> Optional[str]:
        """
        (Optional) If the document was converted to PDF from another format,
        the name of the conforming product that created the original document
        from which it was converted.
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["Creator"]
        except:
            return None

    def get_author(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The name of the person who created the document.
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["Author"]
        except:
            return None

    def get_creation_date(self) -> Optional[str]:
        """
        (Optional) The date and time the document was created, in human-
        readable form (see 7.9.4, “Dates”).
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["CreationDate"]
        except:
            return None

    def get_modification_date(self) -> Optional[str]:
        """
        Required if PieceInfo is present in the document catalogue;
        otherwise optional; PDF 1.1) The date and time the document was
        most recently modified, in human-readable form (see 7.9.4, “Dates”).
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["ModDate"]
        except:
            return None

    def get_subject(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The subject of the document.
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["Subject"]
        except:
            return None

    def get_keywords(self) -> Optional[List[str]]:
        """
        (Optional; PDF 1.1) Keywords associated with the document.
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["Keywords"]
        except:
            return None

    def get_producer(self) -> Optional[str]:
        """
        (Optional) If the document was converted to PDF from another format,
        the name of the conforming product that converted it to PDF.
        """
        try:
            return self._document["XRef"]["Trailer"]["Info"]["Producer"]
        except:
            return None

    def get_number_of_pages(self) -> Optional[Decimal]:
        """
        This function returns the number of pages in the Document
        """
        return self._document["XRef"]["Trailer"]["Root"]["Pages"]["Count"]

    def get_file_size(self) -> Optional[int]:
        """
        This function returns the filesize (in bytes) of this Document
        """
        return int(self._document("FileSize"))

    def get_ids(self) -> Optional[List[str]]:
        """
        File identifiers shall be defined by the optional ID entry in a PDF file’s trailer dictionary (see 7.5.5, “File Trailer”).
        The ID entry is optional but should be used. The value of this entry shall be an array of two byte strings. The
        first byte string shall be a permanent identifier based on the contents of the file at the time it was originally
        created and shall not change when the file is incrementally updated. The second byte string shall be a
        changing identifier based on the file’s contents at the time it was last updated. When a file is first written, both
        identifiers shall be set to the same value. If both identifiers match when a file reference is resolved, it is very
        likely that the correct and unchanged file has been found. If only the first identifier matches, a different version
        of the correct file has been found.
        """
        if (
            "XRef" in self._document
            and "Trailer" in self._document["XRef"]
            and "ID" in self._document["XRef"]["Trailer"]
        ):
            return self._document["XRef"]["Trailer"]["ID"]
        return None

    def get_language(self) -> Optional[str]:
        """
        (Optional; PDF 1.4) A language identifier that shall specify the
        natural language for all text in the document except where
        overridden by language specifications for structure elements or
        marked content (see 14.9.2, "Natural Language Specification"). If
        this entry is absent, the language shall be considered unknown.
        """
        try:
            return self._document["XRef"]["Trailer"]["Root"]["Lang"]
        except:
            return None


class XMPDocumentInfo(DocumentInfo):
    """
    This class represents the (XMP) meta-information belonging to a PDF document
    """

    def __init__(self, document: "Document"):  # type: ignore [name-defined]
        super(XMPDocumentInfo, self).__init__(document)

    def get_creation_date(self) -> Optional[str]:
        """
        (Optional) The date and time the document was created, in human-
        readable form (see 7.9.4, “Dates”).
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}CreateDate")[0]
                .text
            )
        except:
            return None

    def get_modification_date(self) -> Optional[str]:
        """
        Required if PieceInfo is present in the document catalogue;
        otherwise optional; PDF 1.1) The date and time the document was
        most recently modified, in human-readable form (see 7.9.4, “Dates”).
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}ModifyDate")[0]
                .text
            )
        except:
            return None

    def get_metadata_date(self) -> Optional[str]:
        """
        (Optional) The date and time the metadata for this document was created, in human-
        readable form (see 7.9.4, “Dates”).
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}MetadataDate")[0]
                .text
            )
        except:
            return None

    def get_title(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The document’s title.
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}title")[0]
                .text
            )
        except:
            return None

    def get_creator(self) -> Optional[str]:
        """
        (Optional) If the document was converted to PDF from another format,
        the name of the conforming product that created the original document
        from which it was converted.
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}creator")[0]
                .text
            )
        except:
            return None

    def get_publisher(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The name of the person/software who/which published the document.
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}publisher")[0]
                .text
            )
        except:
            return None

    def get_instance_id(self) -> Optional[str]:
        """
        An identifier for a specific incarnation of a document, updated each time a file is saved.
        It should be based on a UUID; see Document and Instance IDs.
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}InstanceID")[0]
                .text
            )
        except:
            return None

    def get_original_document_id(self) -> Optional[str]:
        """
        Refer to Part 1, Data Model, Serialization, and Core Properties, for definition.
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}OriginalDocumentID")[0]
                .text
            )
        except:
            return None

    def get_document_id(self) -> Optional[str]:
        """
        The common identifier for all versions and renditions of a document.
        It should be based on a UUID; see Document and Instance IDs.
        """
        try:
            return (
                self._document["XRef"]["Trailer"]["Root"]["Metadata"]
                .findall(".//{*}DocumentID")[0]
                .text
            )
        except:
            return None
