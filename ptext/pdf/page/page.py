from ptext.io.read_transform.types import Dictionary
from ptext.pdf.page.page_info import PageInfo


class Page(Dictionary):
    def get_page_info(self) -> PageInfo:
        return PageInfo(self)

    def get_document(self) -> "Document":  # type: ignore [name-defined]
        return self.get_root()  # type: ignore [attr-defined]
