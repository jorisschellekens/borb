#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class represents a PDF document
"""
import typing
from decimal import Decimal

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary, List, Name, Stream, String
from borb.pdf.page.page import DestinationType, Page
from borb.pdf.trailer.document_info import DocumentInfo, XMPDocumentInfo
from borb.pdf.xref.plaintext_xref import PlainTextXREF


class Document(Dictionary):
    """
    This class represents a PDF document
    """

    def get_document_info(self) -> DocumentInfo:
        """
        This function returns the DocumentInfo of this Document
        """
        return DocumentInfo(self)

    def get_xmp_document_info(self) -> XMPDocumentInfo:
        """
        This function returns the XMPDocumentInfo of this Document
        """
        return XMPDocumentInfo(self)

    def get_page(self, page_number: int) -> Page:
        """
        This function returns a Page (at given page_number) within this Document
        """
        return self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][page_number]

    def append_document(self, document: "Document") -> "Document":
        """
        This method appends another Document to this one
        """
        number_of_pages_in_other = int(
            document.get_document_info().get_number_of_pages() or 0
        )
        for i in range(0, number_of_pages_in_other):
            self.append_page(document.get_page(i))
        return self

    def append_page(self, page: Page) -> "Document":  # type: ignore [name-defined]
        """
        This method appends a page (from another Document) to this Document
        """
        return self.insert_page(page)

    def insert_page(self, page: Page, index: typing.Optional[int] = None) -> "Document":  # type: ignore [name-defined]
        """
        This method appends a page (from another Document) to this Document at a given index
        """
        # build XRef
        if "XRef" not in self:
            self[Name("XRef")] = PlainTextXREF()
            self[Name("XRef")].set_parent(self)
        # build Trailer
        if "Trailer" not in self["XRef"]:
            self["XRef"][Name("Trailer")] = Dictionary()
            self["XRef"][Name("Size")] = bDecimal(0)
            self["XRef"]["Trailer"].set_parent(self["XRef"])
        # build Root
        if "Root" not in self["XRef"]["Trailer"]:
            self["XRef"]["Trailer"][Name("Root")] = Dictionary()
            self["XRef"]["Trailer"]["Root"][Name("Type")] = Name("Catalog")
            self["XRef"]["Trailer"]["Root"].set_parent(self["XRef"]["Trailer"])
        # build Pages
        if "Pages" not in self["XRef"]["Trailer"]["Root"]:
            # fmt: off
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")] = Dictionary()
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][Name("Count")] = bDecimal(0)
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][Name("Kids")] = List()
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][Name("Type")] = Name("Pages")
            self["XRef"]["Trailer"]["Root"]["Pages"].set_parent(self["XRef"]["Trailer"]["Root"])
            self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"].set_parent(self["XRef"]["Trailer"]["Root"]["Pages"])
            # fmt: on
        # update /Kids
        kids = self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"]
        assert kids is not None
        assert isinstance(kids, List)
        if index is None:
            index = len(kids)
        kids.insert(index, page)
        # update /Count
        prev_count = self["XRef"]["Trailer"]["Root"]["Pages"]["Count"]
        self["XRef"]["Trailer"]["Root"]["Pages"][Name("Count")] = bDecimal(
            prev_count + 1
        )
        # set /Parent
        page[Name("Parent")] = self["XRef"]["Trailer"]["Root"]["Pages"]
        page.set_parent(kids)  # type: ignore [attr-defined]
        # return
        return self

    def pop_page(self, index: int) -> "Document":  # type: ignore [name-specified]
        """
        This method removes a Page from this Document at a given index.
        It then returns this Document.
        """
        if "XRef" not in self:
            return self
        if "Trailer" not in self["XRef"]:
            return self
        if "Root" not in self["XRef"]["Trailer"]:
            return self
        if "Pages" not in self["XRef"]["Trailer"]["Root"]:
            return self
        if "Kids" not in self["XRef"]["Trailer"]["Root"]["Pages"]:
            return self
        if "Count" not in self["XRef"]["Trailer"]["Root"]["Pages"]:
            return self

        # get Kids
        kids = self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"]
        assert kids is not None
        assert isinstance(kids, List)

        # out of bounds
        if index < 0 or index >= len(kids):
            return self

        # remove
        kids.pop(index)
        self["XRef"]["Trailer"]["Root"]["Pages"][Name("Count")] = bDecimal(len(kids))

        # return
        return self

    def has_signatures(self) -> bool:
        """
        This function returns True if this Document has signatures, False otherwise
        """
        # TODO
        return False

    def check_signatures(self) -> bool:
        """
        This method verifies the signatures in the Document,
        it returns True if the signatures match the digest of the Document
        (or if the Document has no signatures), False otherwise
        """
        # TODO
        return True

    def has_outlines(self) -> bool:
        """
        A PDF document may contain a document outline that the conforming reader may display on the screen,
        allowing the user to navigate interactively from one part of the document to another. The outline consists of a
        tree-structured hierarchy of outline items (sometimes called bookmarks), which serve as a visual table of
        contents to display the document’s structure to the user.
        This function returns True if this Document has outlines, false otherwise
        """
        try:
            return (
                "Outlines" in self["XRef"]["Trailer"]["Root"]
                and "Count" in self["XRef"]["Trailer"]["Root"]["Outlines"]
                and self["XRef"]["Trailer"]["Root"]["Outlines"]["Count"] > 0
            )
        except:
            return False

    def add_outline(
        self,
        text: str,
        level: int,
        destination_type: DestinationType,
        page_nr: int,
        top: typing.Optional[Decimal] = None,
        right: typing.Optional[Decimal] = None,
        bottom: typing.Optional[Decimal] = None,
        left: typing.Optional[Decimal] = None,
        zoom: typing.Optional[Decimal] = None,
    ) -> "Document":
        """
        A PDF document may contain a document outline that the conforming reader may display on the screen,
        allowing the user to navigate interactively from one part of the document to another. The outline consists of a
        tree-structured hierarchy of outline items (sometimes called bookmarks), which serve as a visual table of
        contents to display the document’s structure to the user.
        This function adds an outline to this Document
        """
        destination = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        destination.append(bDecimal(page_nr))
        destination.append(destination_type.value)
        if destination_type == DestinationType.X_Y_Z:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is not None
                and zoom is not None
            )
            destination.append(bDecimal(left))
            destination.append(bDecimal(top))
            destination.append(bDecimal(zoom))
        if destination_type == DestinationType.FIT:
            assert (
                left is None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
        if destination_type == DestinationType.FIT_H:
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(bDecimal(top))
        if destination_type == DestinationType.FIT_V:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(bDecimal(left))
        if destination_type == DestinationType.FIT_R:
            assert (
                left is not None
                and bottom is not None
                and right is not None
                and top is not None
                and zoom is None
            )
            destination.append(bDecimal(left))
            destination.append(bDecimal(bottom))
            destination.append(bDecimal(right))
            destination.append(bDecimal(top))
        if destination_type == DestinationType.FIT_B_H:
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(bDecimal(top))
        if destination_type == DestinationType.FIT_B_V:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(bDecimal(left))

        # add \Outlines entry in \Root
        if "Outlines" not in self["XRef"]["Trailer"]["Root"]:
            outline_dictionary: Dictionary = Dictionary()
            self["XRef"]["Trailer"]["Root"][Name("Outlines")] = outline_dictionary
            outline_dictionary.set_parent(  # type: ignore [attr-defined]
                self["XRef"]["Trailer"]["Root"][Name("Outlines")]
            )
            outline_dictionary[Name("Type")] = Name("Outlines")
            outline_dictionary[Name("Count")] = bDecimal(0)

        # create entry
        outline = Dictionary()
        outline[Name("Dest")] = destination
        outline[Name("Parent")] = None
        outline[Name("Title")] = String(text)

        # get \Outlines
        outline_dictionary = self["XRef"]["Trailer"]["Root"]["Outlines"]

        # if everything is empty, add the new entry as the only entry
        if "First" not in outline_dictionary or "Last" not in outline_dictionary:
            outline_dictionary[Name("First")] = outline
            outline_dictionary[Name("Last")] = outline
            outline_dictionary[Name("Count")] = bDecimal(1)
            outline[Name("Parent")] = outline_dictionary
            return self

        # helper function to make DFS easier
        def _children(x: Dictionary):
            if "First" not in x:
                return []
            children = [x["First"]]
            while children[-1] != x["Last"]:
                children.append(children[-1]["Next"])
            return children

        # DFS outline(s)
        outlines_done: typing.List[typing.Tuple[int, Dictionary]] = []
        outlines_todo: typing.List[typing.Tuple[int, Dictionary]] = [
            (-1, outline_dictionary)
        ]
        while len(outlines_todo) > 0:
            t = outlines_todo[0]
            outlines_done.append(t)
            outlines_todo.pop(0)
            for c in _children(t[1]):
                outlines_todo.append((t[0] + 1, c))

        # find parent
        parent = [x[1] for x in outlines_done if x[0] == level - 1][-1]

        # update sibling-linking
        if "Last" in parent:
            sibling = parent["Last"]
            sibling[Name("Next")] = outline

        # update parent-linking
        outline[Name("Parent")] = parent
        if "First" not in parent:
            parent[Name("First")] = outline
        if "Count" not in parent:
            parent[Name("Count")] = bDecimal(0)
        parent[Name("Last")] = outline

        # update count
        outline_to_update_count = parent
        while outline_to_update_count:
            outline_to_update_count[Name("Count")] = bDecimal(
                outline_to_update_count["Count"] + Decimal(1)
            )
            if "Parent" in outline_to_update_count:
                outline_to_update_count = outline_to_update_count["Parent"]
            else:
                break

        return self

    def append_embedded_file(self, file_name: str, file_bytes: bytes) -> "Document":
        """
        If a PDF file contains file specifications that refer to an external file and the PDF file is archived or transmitted,
        some provision should be made to ensure that the external references will remain valid. One way to do this is to
        arrange for copies of the external files to accompany the PDF file. Embedded file streams (PDF 1.3) address
        this problem by allowing the contents of referenced files to be embedded directly within the body of the PDF
        file. This makes the PDF file a self-contained unit that can be stored or transmitted as a single entity. (The
        embedded files are included purely for convenience and need not be directly processed by any conforming reader.)
        This method embeds a file (specified by its name and bytes) into this Document
        """
        assert "XRef" in self
        assert "Trailer" in self["XRef"]
        assert "Root" in self["XRef"]["Trailer"]
        root = self["XRef"]["Trailer"]["Root"]

        # set up /Names dictionary
        if "Names" not in root:
            root[Name("Names")] = Dictionary()
        names = root["Names"]

        # set up /EmbeddedFiles
        if "EmbeddedFiles" not in names:
            names[Name("EmbeddedFiles")] = Dictionary()
            names["EmbeddedFiles"][Name("Kids")] = List()

        # find parent
        parent = names["EmbeddedFiles"]
        while "Kids" in parent:
            for k in parent["Kids"]:
                lower_limit = str(k["Limits"][0])
                upper_limit = str(k["Limits"][1])
                if lower_limit == upper_limit:
                    continue
                if lower_limit < file_name < upper_limit:
                    parent = k
                    break
            break

        # add new child
        if (
            len(
                [
                    x
                    for x in parent["Kids"]
                    if x["Limits"][0] == x["Limits"][1] == file_name
                ]
            )
            == 0
        ):

            kid = Dictionary()
            kid[Name("F")] = String(file_name)
            kid[Name("Type")] = Name("Filespec")
            kid[Name("Limits")] = List()
            for _ in range(0, 2):
                kid["Limits"].append(String(file_name))

            # build leaf \Names dictionary
            names = List()
            names.append(String(file_name))
            kid[Name("Names")] = names

            # build actual file stream
            stream = Stream()
            stream[Name("Type")] = Name("EmbeddedFile")
            stream[Name("Bytes")] = file_bytes
            stream[Name("Length")] = bDecimal(len(stream[Name("Bytes")]))

            # build leaf \Filespec dictionary
            file_spec = Dictionary()
            file_spec[Name("EF")] = Dictionary()
            file_spec["EF"][Name("F")] = stream
            file_spec[Name("F")] = String(file_name)
            file_spec[Name("Type")] = Name("Filespec")
            names.append(file_spec)

            # append
            parent["Kids"].append(kid)

        # change existing child
        else:
            kid = [
                x
                for x in parent["Kids"]
                if x["Limits"][0] == x["Limits"][1] == file_name
            ][0]
            # TODO

        # return
        return self

    def get_embedded_files(self) -> typing.Dict[str, bytes]:
        """
        If a PDF file contains file specifications that refer to an external file and the PDF file is archived or transmitted,
        some provision should be made to ensure that the external references will remain valid. One way to do this is to
        arrange for copies of the external files to accompany the PDF file. Embedded file streams (PDF 1.3) address
        this problem by allowing the contents of referenced files to be embedded directly within the body of the PDF
        file. This makes the PDF file a self-contained unit that can be stored or transmitted as a single entity. (The
        embedded files are included purely for convenience and need not be directly processed by any conforming reader.)
        This method returns all embedded files, as a dictionary of names unto bytes
        """
        assert "XRef" in self
        assert "Trailer" in self["XRef"]
        assert "Root" in self["XRef"]["Trailer"]
        root = self["XRef"]["Trailer"]["Root"]

        # look up /Names dictionary
        if "Names" not in root:
            return {}
        names = root["Names"]

        # look up /EmbeddedFiles dictionary
        if "EmbeddedFiles" not in names:
            return {}

        nodes_to_visit = [names["EmbeddedFiles"]]
        file_names = []
        while len(nodes_to_visit) > 0:
            n = nodes_to_visit[0]
            nodes_to_visit.pop(0)
            if "Kids" in n:
                for k in n["Kids"]:
                    nodes_to_visit.append(k)
            if "Limits" in n:
                lower_limit = str(n["Limits"][0])
                upper_limit = str(n["Limits"][1])
                if upper_limit == lower_limit:
                    file_names.append(upper_limit)

        file_names_and_contents: typing.Dict[str, bytes] = {}
        for n in file_names:
            contents = self.get_embedded_file(n)
            assert contents is not None
            file_names_and_contents[n] = contents

        # return
        return file_names_and_contents

    def get_embedded_file(self, file_name: str) -> typing.Optional[bytes]:
        """
        If a PDF file contains file specifications that refer to an external file and the PDF file is archived or transmitted,
        some provision should be made to ensure that the external references will remain valid. One way to do this is to
        arrange for copies of the external files to accompany the PDF file. Embedded file streams (PDF 1.3) address
        this problem by allowing the contents of referenced files to be embedded directly within the body of the PDF
        file. This makes the PDF file a self-contained unit that can be stored or transmitted as a single entity. (The
        embedded files are included purely for convenience and need not be directly processed by any conforming reader.)
        This method returns the embedded file specified by the given file_name
        """
        assert "XRef" in self
        assert "Trailer" in self["XRef"]
        assert "Root" in self["XRef"]["Trailer"]
        root = self["XRef"]["Trailer"]["Root"]

        # look up /Names dictionary
        if "Names" not in root:
            return None
        names = root["Names"]

        # look up /EmbeddedFiles dictionary
        if "EmbeddedFiles" not in names:
            return None

        # find parent
        parent = names["EmbeddedFiles"]
        while "Kids" in parent:
            for k in parent["Kids"]:
                lower_limit = str(k["Limits"][0])
                upper_limit = str(k["Limits"][1])
                if lower_limit == upper_limit == file_name:
                    assert "Names" in k
                    assert isinstance(k["Names"], list)
                    assert len(k["Names"]) == 2
                    assert str(k["Names"][0]) == file_name

                    # go to /FileSpec leaf
                    file_spec_leaf = k["Names"][1]
                    assert isinstance(file_spec_leaf, dict)
                    assert "EF" in file_spec_leaf
                    assert isinstance(file_spec_leaf["EF"], dict)
                    assert "F" in file_spec_leaf["EF"]
                    assert isinstance(file_spec_leaf["EF"]["F"], Stream)

                    # extract bytes from Stream
                    return file_spec_leaf["EF"]["F"]["DecodedBytes"]

                if lower_limit < file_name < upper_limit:
                    parent = k
                    break
            break

        # default
        return None
