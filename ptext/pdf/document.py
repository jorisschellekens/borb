from ptext.pdf.trailer.document_info import DocumentInfo
from ptext.io.transform.types import DictionaryWithParentAttribute


class Document(DictionaryWithParentAttribute):
    def get_document_info(self) -> "DocumentInfo":
        return DocumentInfo(self)

    def get_page(self, page_number) -> "Page":
        return self.get(["XRef", "Trailer", "Root", "Pages", "Kids", page_number])
