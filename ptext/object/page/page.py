from ptext.object.page.page_info import PageInfo
from ptext.tranform.types_with_parent_attribute import DictionaryWithParentAttribute


class Page(DictionaryWithParentAttribute):
    def get_page_info(self) -> PageInfo:
        return PageInfo(self)
