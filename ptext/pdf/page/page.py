from ptext.pdf.page.page_info import PageInfo
from ptext.io.transform.types import DictionaryWithParentAttribute


class Page(DictionaryWithParentAttribute):
    def get_page_info(self) -> PageInfo:
        return PageInfo(self)
