from ptext.object.document.document_info import DocumentInfo
from ptext.object.pdf_high_level_object import PDFHighLevelObject


class Document(PDFHighLevelObject):
    def get_document_info(self) -> "DocumentInfo":
        return DocumentInfo(self)

    def get_page(self, page_number) -> "Page":
        return self.get(["XRef", "Trailer", "Root", "Pages", "Kids", page_number])
