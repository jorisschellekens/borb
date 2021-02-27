from ptext.pdf.canvas.layout.list import OrderedList, UnorderedList
from ptext.pdf.canvas.layout.page_layout import PageLayout
from ptext.pdf.canvas.layout.paragraph import (
    LayoutElement,
    Paragraph,
    ChunkOfText,
    LineOfText,
    Heading,
)
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.page.page import Page


class StyledPageLayout(PageLayout):
    def __init__(self, page_layout: PageLayout, page: Page):
        super().__init__(page)
        self.page_layout = page_layout

    def add(self, layout_element: LayoutElement) -> "PageLayout":

        # change LayoutElement
        if isinstance(layout_element, Paragraph):
            self._change_paragraph(layout_element)

        # call inner layout
        self.page_layout.add(layout_element)

        # return self
        return self

    def _change_chunk_of_text(self, chunk_of_text: ChunkOfText):
        pass

    def _change_line_of_text(self, chunk_of_text: LineOfText):
        pass

    def _change_paragraph(self, paragraph: Paragraph):
        pass

    def _change_heading(self, heading: Heading):
        pass

    def _change_ordered_list(self, ordered_list: OrderedList):
        pass

    def _change_unordered_list(self, unordered_list: UnorderedList):
        pass

    def _change_table(self, table: Table):
        pass
