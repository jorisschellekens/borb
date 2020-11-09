from ptext.object.page.page_info import PageInfo
from ptext.object.pdf_high_level_object import PDFHighLevelObject


class Page(PDFHighLevelObject):
    def __init__(self):
        super().__init__()

    def get_page_info(self) -> PageInfo:
        return PageInfo(self)
