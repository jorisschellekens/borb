from ptext.io.read_transform.types import Dictionary, Decimal, List, Name
from ptext.pdf.page.page import Page
from ptext.pdf.trailer.document_info import DocumentInfo, XMPDocumentInfo
from ptext.pdf.xref.plaintext_xref import PlainTextXREF


class Document(Dictionary):
    def get_document_info(self) -> DocumentInfo:
        return DocumentInfo(self)

    def get_xmp_document_info(self) -> XMPDocumentInfo:
        return XMPDocumentInfo(self)

    def get_page(self, page_number: int) -> Page:
        return self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][page_number]

    def append_document(self, document: "Document") -> "Document":
        number_of_pages_in_other = int(
            document.get_document_info().get_number_of_pages() or 0
        )
        for i in range(0, number_of_pages_in_other):
            self.append_page(document.get_page(i))
        return self

    def append_page(self, page: Page) -> "Document":  # type: ignore [name-defined]
        return self.insert_page(page, -1)

    def insert_page(self, page: Page, index: int = -1) -> "Document":  # type: ignore [name-defined]
        # build XRef
        if "XRef" not in self:
            self["XRef"] = PlainTextXREF()
        # build Trailer
        if "Trailer" not in self["XRef"]:
            self["XRef"]["Trailer"] = Dictionary()
            self["XRef"][Name("Size")] = Decimal(0)
        # build Root
        if "Root" not in self["XRef"]["Trailer"]:
            self["XRef"]["Trailer"][Name("Root")] = Dictionary()
        # build Pages
        if "Pages" not in self["XRef"]["Trailer"]["Root"]:
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")] = Dictionary()
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][
                Name("Count")
            ] = Decimal(0)
            self["XRef"]["Trailer"][Name("Root")][Name("Pages")][Name("Kids")] = List()
        # update /Kids
        kids = self["XRef"]["Trailer"]["Root"]["Pages"]["Kids"]
        assert kids is not None
        assert isinstance(kids, List)
        kids.insert(index, page)
        # update /Count
        prev_count = self["XRef"]["Trailer"]["Root"]["Pages"]["Count"]
        self["XRef"]["Trailer"]["Root"]["Pages"]["Count"] = Decimal(prev_count + 1)
        # return
        return self

    def pop_page(self, index: int) -> "Document":  # type: ignore [name-specified]
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

    def has_signatures(self):
        return False

    def check_signatures(self):
        pass
