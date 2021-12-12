import typing

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.page.page import Page


class BoxLayout(PageLayout):
    def __init__(self, page: Page, boxes: typing.List[Rectangle]):
        super(BoxLayout, self).__init__(page)
        assert len(boxes) > 0
        self._boxes: typing.List[Rectangle] = boxes

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        return self
