import typing
from decimal import Decimal

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import LayoutElement, ChunkOfText
from ptext.pdf.page.page import Page


class UnorderedList(LayoutElement):
    def __init__(self):
        self.items: typing.List[LayoutElement] = []

    def add(self, element: LayoutElement):
        self.items.append(element)

    def layout(self, page: Page, bounding_box: Rectangle) -> Rectangle:
        last_item_bottom: Decimal = bounding_box.y + bounding_box.height
        bullet_margin: Decimal = Decimal(20)
        for i in self.items:
            # bullet character
            ChunkOfText(
                text="0",
                font_size=Decimal(12),
                font_color=X11Color("Black"),  # TODO use bullet character
            ).layout(
                page=page,
                bounding_box=Rectangle(
                    bounding_box.x,
                    bounding_box.y,
                    bullet_margin,
                    last_item_bottom - bounding_box.y,
                ),
            )
            # content
            item_rect = i.layout(
                page,
                bounding_box=Rectangle(
                    bounding_box.x + bullet_margin,
                    bounding_box.y,
                    bounding_box.width - bullet_margin,
                    last_item_bottom - bounding_box.y,
                ),
            )
            # set new last_item_bottom
            last_item_bottom = item_rect.y
        return Rectangle(
            bounding_box.x,
            last_item_bottom,
            bounding_box.width,
            bounding_box.y + bounding_box.height - last_item_bottom,
        )


class OrderedList(LayoutElement):
    def __init__(self, index_offset: int = 0):
        self.items: typing.List[LayoutElement] = []
        self.index_offset = index_offset

    def add(self, element: LayoutElement):
        self.items.append(element)

    def layout(self, page: Page, bounding_box: Rectangle) -> Rectangle:
        last_item_bottom: Decimal = bounding_box.y + bounding_box.height
        bullet_margin: Decimal = Decimal(20)
        for index, i in enumerate(self.items):
            # bullet character
            ChunkOfText(
                text=str(index + 1 + self.index_offset) + ".",
                font_size=Decimal(12),
                font_color=X11Color("Black"),
            ).layout(
                page=page,
                bounding_box=Rectangle(
                    bounding_box.x,
                    bounding_box.y,
                    bullet_margin,
                    last_item_bottom - bounding_box.y,
                ),
            )
            # content
            item_rect = i.layout(
                page,
                bounding_box=Rectangle(
                    bounding_box.x + bullet_margin,
                    bounding_box.y,
                    bounding_box.width - bullet_margin,
                    last_item_bottom - bounding_box.y,
                ),
            )
            # set new last_item_bottom
            last_item_bottom = item_rect.y
        return Rectangle(
            bounding_box.x,
            last_item_bottom,
            bounding_box.width,
            bounding_box.y + bounding_box.height - last_item_bottom,
        )
