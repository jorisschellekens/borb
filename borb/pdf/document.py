#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a PDF document, providing functionality to create, manipulate, and export PDF files.

The Document class allows for adding and organizing pages, embedding various types of content
such as text, images, and tables, and managing features like metadata, encryption, and annotations.
It serves as the main structure for building and editing PDF documents, offering control over
the document's layout and content.

Instances of this class can be serialized to standard PDF format for viewing, sharing, or printing.
"""

import datetime
import typing

from borb.pdf.conformance import Conformance
from borb.pdf.page import Page
from borb.pdf.primitives import name, hexstr, PDFType, datestr


class Document(dict):
    """
    Represents a PDF document with functionality to create, manipulate, and export PDF files.

    The Document class allows for adding and organizing pages, embedding various types
    of content such as text, images, and tables, and managing features like metadata,
    encryption, and annotations. It serves as the primary structure for building and
    editing PDF documents, offering control over the document's layout and content.

    Instances of this class can be serialized to standard PDF format for viewing,
    sharing, or printing.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        conformance: typing.Optional[Conformance] = None,
        on_non_conformance_print_warning: bool = True,
        on_non_conformance_throw_assert: bool = False,
    ):
        """
        Initialize a new instance of the `Document` class.

        This constructor sets up the document with an optional conformance level.
        The conformance level defines the PDF compliance standards (such as PDF/A)
        the document is intended to meet. If no conformance level is specified,
        the document will not be bound to any particular compliance level upon creation.

        :param conformance: An optional `Conformance` value indicating the
                            desired compliance standard for the document (e.g.,
                            PDF/A-1, PDF/A-2, etc.). If `None`, no specific
                            conformance is set at document creation.
        """
        super().__init__()
        self.__conformance_at_create: typing.Optional[Conformance] = conformance
        self.__on_non_conformance_print_warning: bool = on_non_conformance_print_warning
        self.__on_non_conformance_throw_assert: bool = on_non_conformance_throw_assert

    #
    # PRIVATE
    #

    @staticmethod
    def __get_now_as_date_str() -> str:
        return datestr(datetime.datetime.now().strftime("D:%Y%m%d%H%M%SZ00"))

    @staticmethod
    def __get_random_id() -> hexstr:
        import random

        return hexstr(
            "".join([random.choice("0123456789ABCDEF") for _ in range(0, 32)])
        )

    def __setup_document_skeleton(self) -> None:
        # /XRef
        if "XRef" not in self:
            self[name("XRef")] = {}

        # /Trailer
        if "Trailer" not in self:
            self[name("Trailer")] = {}

        # /Trailer /ID
        if "ID" not in self["Trailer"]:
            self["Trailer"][name("ID")] = [Document.__get_random_id()]
            self["Trailer"][name("ID")] += [self["Trailer"]["ID"][0]]

        # /Trailer /Info
        if "Info" not in self["Trailer"]:
            self["Trailer"][name("Info")] = {}

        # /Trailer /Info /CreationDate
        if "CreationDate" not in self["Trailer"]["Info"]:
            self["Trailer"]["Info"][
                name("CreationDate")
            ] = Document.__get_now_as_date_str()

        # /Trailer /Info /ModDate
        if "ModDate" not in self["Trailer"]["Info"]:
            self["Trailer"]["Info"][name("ModDate")] = Document.__get_now_as_date_str()

        # /Trailer /Info /Producer
        if "Producer" not in self["Trailer"]["Info"]:
            self["Trailer"]["Info"][name("Producer")] = "borb"

        # /Trailer /Root
        if "Root" not in self["Trailer"]:
            self["Trailer"][name("Root")] = {}

        # /Trailer /Root /Type
        if "Type" not in self["Trailer"]["Root"]:
            self["Trailer"]["Root"][name("Type")] = name("Catalog")

        # /Trailer /Root /Pages
        if "Pages" not in self["Trailer"]["Root"]:
            self["Trailer"]["Root"][name("Pages")] = {}

        # /Trailer /Root /Pages /Type
        if "Type" not in self["Trailer"]["Root"]["Pages"]:
            self["Trailer"]["Root"]["Pages"][name("Type")] = name("Pages")

        # /Trailer /Root /Pages /Count
        if "Count" not in self["Trailer"]["Root"]["Pages"]:
            self["Trailer"]["Root"]["Pages"][name("Count")] = 0

        # /Trailer /Root /Pages /Kids
        if "Kids" not in self["Trailer"]["Root"]["Pages"]:
            self["Trailer"]["Root"]["Pages"][name("Kids")] = []

    #
    # PUBLIC
    #

    def append_document(self, other: "Document") -> "Document":
        """
        Append all pages of another Document to this Document.

        This method initializes the document structure (if needed) and sequentially
        appends each page from the given `other` Document to the current Document.

        :param other:   The Document whose pages should be appended.
        :returns:       The modified Document instance with the appended pages.
        """
        # setup (document) skeleton
        self.__setup_document_skeleton()

        # append all pages
        for i in range(0, other.get_number_of_pages()):
            self.append_page(page=other.get_page(i))

        # return
        return self

    def append_page(self, page: Page) -> "Document":
        """
        Append a Page object to the document.

        This method adds the specified page to the end of the document's list of pages. It modifies
        the document in place and returns the updated Document object, allowing for method chaining.

        :param page:    the Page to append
        :return:        self
        """
        # setup (document) skeleton
        self.__setup_document_skeleton()

        # add page
        self["Trailer"]["Root"]["Pages"]["Kids"] += [page]
        self["Trailer"]["Root"]["Pages"]["Count"] += 1

        # link Page to parent
        page[name("Parent")] = self["Trailer"]["Root"]["Pages"]

        # link Page to Document
        page._Page__document = self  # type: ignore[attr-defined]

        # return
        return self

    def get_author(self) -> typing.Optional[str]:
        """
        Retrieve the author information from the PDF document's metadata, if available.

        This method accesses the "Trailer" dictionary of the PDF, navigating to the "Info"
        dictionary to extract the "Author" entry. The author field typically provides the
        name of the individual or organization that created the document.

        :return: A string representing the author of the document, or `None` if the author
                 information is not available.
        """
        return self.get("Trailer", {}).get("Info", {}).get("Author", None)

    def get_conformance_at_create(self) -> typing.Optional[Conformance]:
        """
        Retrieve the conformance set when the document was created.

        This method returns the conformance that was assigned at the time of document creation.
        This may differ from the conformance upon reading the document.

        :return: The `Conformance` set at creation, or `None` if not specified.
        """
        return self.__conformance_at_create

    def get_creation_date(self) -> typing.Optional[datetime.datetime]:
        """
        Retrieve the creation date of the PDF document, if available.

        This method accesses the PDF's "Trailer" dictionary, then navigates to the "Info"
        dictionary to retrieve the "CreationDate" entry. If a creation date is found, it is
        parsed from its expected PDF date format "D:%Y%m%d%H%M%S+00'00'" into a Python
        `datetime` object. If the creation date is missing or cannot be parsed, `None` is returned.

        :return: A `datetime` object representing the document's creation date, or `None`
                 if the creation date is not available or cannot be parsed.
        """
        creation_date_str: typing.Optional[str] = (
            self.get("Trailer", {}).get("Info", {}).get("CreationDate", None)
        )
        if creation_date_str is None:
            return None
        try:
            return datetime.datetime.strptime(
                creation_date_str, "D:%Y%m%d%H%M%S+00'00'"
            )
        except:
            return None

    def get_keywords(self) -> typing.Optional[str]:
        """
        Retrieve the keywords metadata from the PDF document, if available.

        This method accesses the "Trailer" dictionary of the PDF, navigating to the "Info"
        dictionary to extract the "Keywords" entry. The keywords field often contains a
        list of terms or phrases describing the document's content, separated by commas
        or semicolons, intended to aid in document indexing and searchability.

        :return: A string representing the document's keywords, or `None` if no keywords
                 metadata is present.
        """
        return self.get("Trailer", {}).get("Info", {}).get("Keywords", None)

    def get_modification_date(self) -> typing.Optional[datetime.datetime]:
        """
        Retrieve the modification date of the PDF document, if available.

        This method accesses the PDF's "Trailer" dictionary, then navigates to the "Info"
        dictionary to retrieve the "ModDate" entry. If a modification date is found, it is
        parsed from its expected PDF date format "D:%Y%m%d%H%M%S+00'00'" into a Python
        `datetime` object. If the creation date is missing or cannot be parsed, `None` is returned.

        :return: A `datetime` object representing the document's modification date, or `None`
                 if the modification date is not available or cannot be parsed.
        """
        modification_date_str: typing.Optional[str] = (
            self.get("Trailer", {}).get("Info", {}).get("ModDate", None)
        )
        if modification_date_str is None:
            return None
        try:
            return datetime.datetime.strptime(
                modification_date_str, "D:%Y%m%d%H%M%S+00'00'"
            )
        except:
            return None

    def get_number_of_pages(self) -> int:
        """
        Retrieve the number of pages in the PDF document.

        This method accesses the "Trailer" dictionary, navigating through the "Root" dictionary
        to locate the "Pages" dictionary and retrieve the "Count" value, which indicates the total
        number of pages in the document. If this information is unavailable, the method returns 0.

        :return: An integer representing the number of pages in the PDF. Returns 0 if
                 the page count is not specified.
        """
        return self.get("Trailer", {}).get("Root", {}).get("Pages", {}).get("Count", 0)

    def get_page(self, index: int) -> Page:
        """
        Retrieve the Page object at the specified index.

        This method returns the Page object located at the given zero-based index in the document's
        list of pages. If the index is out of range, it raises an IndexError.

        :param index:   the index
        :return:        self
        """
        pages_in_order = [self["Trailer"]["Root"]["Pages"]]
        i: int = 0
        while i < len(pages_in_order):
            n = pages_in_order[i]

            # page tree nodes are exploded and processed in next turn
            if isinstance(n, dict) and "Kids" in n:
                pages_in_order = (
                    pages_in_order[0:i]
                    + [x for x in n["Kids"]]
                    + pages_in_order[i + 1 :]
                )
                continue

            # IF we processed a Page
            # THEN move ahead by 1
            if isinstance(n, Page):
                i += 1

        # return
        return pages_in_order[index]

    def get_producer(self) -> typing.Optional[str]:
        """
        Retrieve the producer information from the PDF document's metadata, if available.

        This method accesses the PDF's "Trailer" dictionary, then navigates to the "Info"
        dictionary to retrieve the "Producer" entry. The producer field generally specifies
        the software or library used to create the PDF document.

        :return: A string representing the producer information, or `None` if the producer
                 information is not available.
        """
        return self.get("Trailer", {}).get("Info", {}).get("Producer", None)

    def get_subject(self) -> typing.Optional[str]:
        """
        Retrieve the subject information from the PDF document's metadata, if available.

        This method accesses the "Trailer" dictionary of the PDF, navigating to the "Info"
        dictionary to extract the "Subject" entry. The subject field typically provides a brief
        description or categorization of the document's content.

        :return: A string representing the subject of the document, or `None` if the subject
                 information is not available.
        """
        return self.get("Trailer", {}).get("Info", {}).get("Subject", None)

    def get_title(self) -> typing.Optional[str]:
        """
        Retrieve the title information from the PDF document's metadata, if available.

        This method accesses the PDF's "Trailer" dictionary, then navigates to the "Info"
        dictionary to retrieve the "Title" entry. The title field generally provides a
        short description or title for the PDF document.

        :return: A string representing the title of the document, or `None` if the title
                 information is not available.
        """
        return self.get("Trailer", {}).get("Info", {}).get("Title", None)

    def insert_page(self, page: Page, index: int = -1) -> "Document":
        """
        Insert a Page object into the document at the specified index.

        This method inserts the given page at the specified position in the document's list of pages.
        If no index is provided or if the index is -1, the page is appended to the end of the document.
        It returns the updated Document object, allowing for method chaining.

        :param page:    the Page to insert
        :param index:   the index at which to insert the Page
        :return:        self
        """
        if index == -1:
            return self.append_page(page)
        if index == self.get_number_of_pages():
            return self.append_page(page)

        # check the index
        assert 0 <= index < self.get_number_of_pages()

        # traverse the page-tree to insert the Page
        page_id_to_parent: typing.Dict[int, PDFType] = {}
        page_nr_to_page: typing.Dict[int, PDFType] = {}
        todo: typing.List[PDFType] = [self["Trailer"]["Root"]["Pages"]]
        while len(todo) > 0:
            n: PDFType = todo.pop()
            # thing has kids
            if isinstance(n, dict) and ("Kids" in n):
                for k in n["Kids"]:  # type: ignore[union-attr]
                    todo = [k] + todo
                    page_id_to_parent[id(k)] = n
            # thing is a Page
            if isinstance(n, Page):
                page_nr_to_page[len(page_nr_to_page)] = n
                continue

        # determine where to insert (in the lowest level page-tree)
        # fmt: off
        prev_page_at_index = page_nr_to_page[index]
        parent = page_id_to_parent[id(page_nr_to_page[index])]
        index_in_kids: int = next(iter([(i, parent['Kids'][i]) for i in range(0, len(parent['Kids'])) if parent['Kids'][i] == prev_page_at_index]))[0] # type: ignore[arg-type, call-overload, index]
        # fmt: on

        # insert, change count
        parent["Kids"].insert(index_in_kids, page)  # type: ignore[call-overload, index, union-attr]
        parent["Count"] += 1  # type: ignore[call-overload, index, operator]

        # propagate up
        while id(parent) in page_id_to_parent and ("Count" in parent):  # type: ignore[operator]
            parent = page_id_to_parent[id(parent)]
            parent["Count"] += 1  # type: ignore[call-overload, index, operator]

        # return
        return self

    def pop_page(self, index: int) -> "Document":
        """
        Remove and return the Page object at the specified index.

        This method removes the page located at the given zero-based index from the document's
        list of pages. The document is modified in place, and the updated Document object
        is returned for method chaining. If the index is out of range, it raises an IndexError.

        :param index:   the index
        :return:        self
        """
        if index == -1:
            index = self.get_number_of_pages() - 1

        # check the index
        assert 0 <= index < self.get_number_of_pages()

        # traverse the page-tree to remove the Page
        page_id_to_parent: typing.Dict[int, PDFType] = {}
        page_nr_to_page: typing.Dict[int, PDFType] = {}
        todo: typing.List[PDFType] = [self["Trailer"]["Root"]["Pages"]]
        while len(todo) > 0:
            n: PDFType = todo.pop()
            # thing has kids
            if isinstance(n, dict) and ("Kids" in n):
                for k in n["Kids"]:  # type: ignore[union-attr]
                    todo = [k] + todo
                    page_id_to_parent[id(k)] = n
            # thing is a Page
            if isinstance(n, Page):
                page_nr_to_page[len(page_nr_to_page)] = n
                continue

        # determine where to remove (in the lowest level page-tree)
        # fmt: off
        prev_page_at_index = page_nr_to_page[index]
        parent = page_id_to_parent[id(page_nr_to_page[index])]
        index_in_kids: int = next(iter([(i, parent['Kids'][i]) for i in range(0, len(parent['Kids'])) if parent['Kids'][i] == prev_page_at_index]))[0] # type: ignore[arg-type, call-overload, index]
        # fmt: on

        # delete
        del parent["Kids"][index_in_kids]  # type: ignore[arg-type, call-overload, index, union-attr]
        parent["Count"] -= 1  # type: ignore[call-overload, index, operator]

        # propagate up
        while id(parent) in page_id_to_parent and ("Count" in parent):  # type: ignore[operator]
            parent = page_id_to_parent[id(parent)]
            parent["Count"] -= 1  # type: ignore[call-overload, index, operator]

        # return
        return self
