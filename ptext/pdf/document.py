#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class represents a PDF document
"""

import typing

from ptext.io.read.types import (
    Dictionary,
    Decimal,
    List,
    Name,
    String,
)
from ptext.pdf.page.page import Page, DestinationType
from ptext.pdf.trailer.document_info import DocumentInfo, XMPDocumentInfo
from ptext.pdf.xref.plaintext_xref import PlainTextXREF


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
            self["XRef"][Name("Size")] = Decimal(0)
            self["XRef"]["Trailer"].set_parent(self["XRef"])
        # build Root
        if "Root" not in self["XRef"]["Trailer"]:
            self["XRef"]["Trailer"][Name("Root")] = Dictionary()
            self["XRef"]["Trailer"]["Root"].set_parent(self["XRef"]["Trailer"])
        # build Pages
        if "Pages" not in self["XRef"]["Trailer"]["Root"]:
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")] = Dictionary()
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][
                Name("Count")
            ] = Decimal(0)
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][Name("Kids")] = List()
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][Name("Type")] = Name(
                "Pages"
            )
            self["XRef"]["Trailer"]["Root"]["Pages"].set_parent(
                self["XRef"]["Trailer"]["Root"]
            )
            self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"].set_parent(
                self["XRef"]["Trailer"]["Root"]["Pages"]
            )
        # update /Kids
        kids = self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"]
        assert kids is not None
        assert isinstance(kids, List)
        if index is None:
            index = len(kids)
        kids.insert(index, page)
        # update /Count
        prev_count = self["XRef"]["Trailer"]["Root"]["Pages"]["Count"]
        self["XRef"]["Trailer"]["Root"]["Pages"][Name("Count")] = Decimal(
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

        # get Kids
        kids = self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"]
        assert kids is not None
        assert isinstance(kids, List)

        # out of bounds
        if index < 0 or index >= len(kids):
            return self

        # remove
        kids.pop(index)

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

        destination = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        destination.append(Decimal(page_nr))
        destination.append(destination_type.value)
        if destination_type == DestinationType.X_Y_Z:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is not None
                and zoom is not None
            )
            destination.append(Decimal(left))
            destination.append(Decimal(top))
            destination.append(Decimal(zoom))
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
            destination.append(Decimal(top))
        if destination_type == DestinationType.FIT_V:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(Decimal(left))
        if destination_type == DestinationType.FIT_R:
            assert (
                left is not None
                and bottom is not None
                and right is not None
                and top is not None
                and zoom is None
            )
            destination.append(Decimal(left))
            destination.append(Decimal(bottom))
            destination.append(Decimal(right))
            destination.append(Decimal(top))
        if destination_type == DestinationType.FIT_B_H:
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(Decimal(top))
        if destination_type == DestinationType.FIT_B_V:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(Decimal(left))

        # add \Outlines entry in \Root
        if "Outlines" not in self["XRef"]["Trailer"]["Root"]:
            outline_dictionary: Dictionary = Dictionary()
            self["XRef"]["Trailer"]["Root"][Name("Outlines")] = outline_dictionary
            outline_dictionary.set_parent(  # type: ignore [attr-defined]
                self["XRef"]["Trailer"]["Root"][Name("Outlines")]
            )
            outline_dictionary[Name("Type")] = Name("Outlines")
            outline_dictionary[Name("Count")] = Decimal(0)

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
            outline_dictionary[Name("Count")] = Decimal(1)
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
            parent[Name("Count")] = Decimal(0)
        parent[Name("Last")] = outline

        # update count
        outline_to_update_count = parent
        while outline_to_update_count:
            outline_to_update_count[Name("Count")] = Decimal(
                outline_to_update_count["Count"] + Decimal(1)
            )
            if "Parent" in outline_to_update_count:
                outline_to_update_count = outline_to_update_count["Parent"]
            else:
                break

        return self
