from ptext.io.transform.types import Dictionary
from ptext.pdf.trailer.document_info import DocumentInfo


class Document(Dictionary):
    def get_document_info(self) -> "DocumentInfo":
        return DocumentInfo(self)

    def get_page(self, page_number) -> "Page":
        return self.get(["XRef", "Trailer", "Root", "Pages", "Kids", page_number])
