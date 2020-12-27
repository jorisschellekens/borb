from ptext.io.transform.types import Dictionary
from ptext.pdf.page.page_info import PageInfo


class Page(Dictionary):
    def get_page_info(self) -> PageInfo:
        return PageInfo(self)
